# Author: Pieter Noordhuis
# Description: Simple demo to showcase Redis PubSub with EventMachine
#
# Update 7 Oct 2010:
# - This example does *not* appear to work with Chrome >=6.0. Apparently,
#   the WebSocket protocol implementation in the cramp gem does not work
#   well with Chrome's (newer) WebSocket implementation.
#
# Requirements:
# - rubygems: eventmachine, thin, cramp, sinatra, yajl-ruby
# - a browser with WebSocket support
#
# Usage:
# ruby redis_pubsub_demo.rb
#

require 'rubygems'
require 'eventmachine'
require 'stringio'
require 'sinatra/base'
require 'cramp/controller'
require 'yajl'

# Incomplete evented Redis implementation specifically made for
# the new PubSub features in Redis.
class EventedRedis < EM::Connection
  def self.connect
    host = (ENV['REDIS_HOST'] || 'localhost')
    port = (ENV['REDIS_PORT'] || 6379).to_i
    EM.connect host, port, self
  end

  def post_init
    @blocks = {}
  end
  
  def subscribe(*channels, &blk)
    channels.each { |c| @blocks[c.to_s] = blk }
    call_command('subscribe', *channels)
  end
  
  def publish(channel, msg)
    call_command('publish', channel, msg)
  end
  
  def unsubscribe
    call_command('unsubscribe')
  end
  
  def receive_data(data)
    buffer = StringIO.new(data)
    begin
      parts = read_response(buffer)
      if parts.is_a?(Array)
        ret = @blocks[parts[1]].call(parts)
        close_connection if ret === false
      end
    end while !buffer.eof?
  end
  
  private
  def read_response(buffer)
    type = buffer.read(1)
    case type
    when ':'
      buffer.gets.to_i
    when '*'
      size = buffer.gets.to_i
      parts = size.times.map { read_object(buffer) }
    else
      raise "unsupported response type"
    end
  end
  
  def read_object(data)
    type = data.read(1)
    case type
    when ':' # integer
      data.gets.to_i
    when '$'
      size = data.gets
      str = data.read(size.to_i)
      data.read(2) # crlf
      str
    else
      raise "read for object of type #{type} not implemented"
    end
  end
  
  # only support multi-bulk
  def call_command(*args)
    command = "*#{args.size}\r\n"
    args.each { |a|
      command << "$#{a.to_s.size}\r\n"
      command << a.to_s
      command << "\r\n"
    }
    send_data command
  end
end

class ChatController < Cramp::Controller::Websocket
  on_start :create_redis
  on_finish :handle_leave, :destroy_redis
  on_data :received_data
  
  def create_redis
    @pub = EventedRedis.connect
    @sub = EventedRedis.connect
  end
  
  def destroy_redis
    @pub.close_connection_after_writing
    @sub.close_connection_after_writing
  end
  
  def received_data(data)
    msg = parse_json(data)
    case msg[:action]
    when 'join'
      handle_join(msg)
    when 'message'
      handle_message(msg)
    else
      # skip
    end
  end
  
  def handle_join(msg)
    @user = msg[:user]
    subscribe
    publish :action => 'control', :user => @user, :message => 'joined the chat room'
  end
  
  def handle_leave
    publish :action => 'control', :user => @user, :message => 'left the chat room'
  end
  
  def handle_message(msg)
    publish msg.merge(:user => @user)
  end
  
  private
  def subscribe
    @sub.subscribe('chat') do |type,channel,message|
      render message
    end
  end
  
  def publish(message)
    @pub.publish('chat', encode_json(message))
  end
  
  def encode_json(obj)
    Yajl::Encoder.encode(obj)
  end
  
  def parse_json(str)
    Yajl::Parser.parse(str, :symbolize_keys => true)
  end
end

class StaticController < Sinatra::Base
  enable :inline_templates
  get('/') { erb :main }
end

EventMachine.run {
  Cramp::Controller::Websocket.backend = :thin
  Rack::Handler::Thin.run ChatController, :Port => 8081
  Rack::Handler::Thin.run StaticController, :Port => 8082
}

__END__
@@ main
<html>
<head>
<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js'></script>
<script src='http://jquery-json.googlecode.com/files/jquery.json-2.2.min.js'></script>
<script src='http://datejs.googlecode.com/svn/trunk/build/date.js'></script>
<script>
$(document).ready(function(){
  if (typeof WebSocket != 'undefined') {
    $('#ask').show();
  } else {
    $('#error').show();
  }
  
  // join on enter
  $('#ask input').keydown(function(event) {
    if (event.keyCode == 13) {
      $('#ask a').click();
    }
  })
  
  // join on click
  $('#ask a').click(function() {
    join($('#ask input').val());
    $('#ask').hide();
    $('#channel').show();
    $('input#message').focus();
  });

  function join(name) {
    var host = window.location.host.split(':')[0];
    var ws = new WebSocket("ws://" + host + ":8081/websocket");

    var container = $('div#msgs');
    ws.onmessage = function(evt) {
      var obj = $.evalJSON(evt.data);
      if (typeof obj != 'object') return;

      var action = obj['action'];
      var struct = container.find('li.' + action + ':first');
      if (struct.length < 1) {
        console.log("Could not handle: " + evt.data);
        return;
      }
      
      var msg = struct.clone();
      msg.find('.time').text((new Date()).toString("HH:mm:ss"));

      if (action == 'message') {
        var matches;
        if (matches = obj['message'].match(/^\s*[\/\\]me\s(.*)/)) {
          msg.find('.user').text(obj['user'] + ' ' + matches[1]);
          msg.find('.user').css('font-weight', 'bold');
        } else {
          msg.find('.user').text(obj['user']);
          msg.find('.message').text(': ' + obj['message']);
        }
      } else if (action == 'control') {
        msg.find('.user').text(obj['user']);
        msg.find('.message').text(obj['message']);
        msg.addClass('control');
      }
      
      if (obj['user'] == name) msg.find('.user').addClass('self');
      container.find('ul').append(msg.show());
      container.scrollTop(container.find('ul').innerHeight());
    }
    
    $('#channel form').submit(function(event) {
      event.preventDefault();
      var input = $(this).find(':input');
      var msg = input.val();
      ws.send($.toJSON({ action: 'message', message: msg }));
      input.val('');
    });
    
    // send name when joining
    ws.onopen = function() {
      ws.send($.toJSON({ action: 'join', user: name }));
    }
  }
});
</script>
<style type="text/css" media="screen">
  * {
    font-family: Georgia;
  }
  a {
    color: #000;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
  div.bordered {
    margin: 0 auto;
    margin-top: 100px;
    width: 600px;
    padding: 20px;
    text-align: center;
    border: 10px solid #ddd;
    -webkit-border-radius: 20px;
  }
  #error {
    background-color: #BA0000;
    color: #fff;
    font-weight: bold;
  }
  #ask {
    font-size: 20pt;
  }
  #ask input {
    font-size: 20pt;
    padding: 10px;
    margin: 0 10px;
  }
  #ask span.join {
    padding: 10px;
    background-color: #ddd;
    -webkit-border-radius: 10px;
  }
  #channel {
    margin-top: 100px;
    height: 480px;
    position: relative;
  }
  #channel div#descr {
    position: absolute;
    left: -10px;
    top: -190px;
    font-size: 13px;
    text-align: left;
    line-height: 20px;
    padding: 5px;
    width: 630px;
  }
  div#msgs {
    overflow-y: scroll;
    height: 400px;
  }
  div#msgs ul {
    list-style: none;
    padding: 0;
    margin: 0;
    text-align: left;
  }
  div#msgs li {
    line-height: 20px;
  }
  div#msgs li span.user {
    color: #ff9900;
  }
  div#msgs li span.user.self {
    color: #aa2211;
  }
  div#msgs li span.time {
    float: right;
    margin-right: 5px;
    color: #aaa;
    font-family: "Courier New";
    font-size: 12px;
  }
  div#msgs li.control {
    text-align: center;
  }
  div#msgs li.control span.message {
    color: #aaa;
  }
  div#input {
    text-align: left;
    margin-top: 20px;
  }
  div#input #message {
    width: 600px;
    border: 5px solid #bbb;
    -webkit-border-radius: 3px;
    font-size: 30pt;
  }
</style>
</head>
<body>
  <a href="http://gist.github.com/348262">
    <img style="position: absolute; top: 0; right: 0; border: 0;" src="http://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub" />
  </a>
  <div id="error" class="bordered" style="display: none;">
    This browser has no native WebSocket support.<br/>
    Use a WebKit nightly or Google Chrome. 
  </div>
  <div id="ask" class="bordered" style="display: none;">
    Name: <input type="text" id="name" /> <a href="#"><span class="join">Join!</span></a>
  </div>
  <div id="channel" class="bordered" style="display: none;">
    <div id="descr" class="bordered">
      <strong>Note:</strong> your messages make a round-trip up and down the stack (including Redis)
      before being displayed here.<br/>
      <strong>Tip:</strong> open up another browser window
      to see how quickly your messages are distributed.
    </div>
    <div id="msgs">
      <ul>
        <li class="message" style="display: none">
          <span class="user"></span><span class="message"></span>
          <span class="time"></span>
        </li>
        <li class="control" style="display: none">
          <span class="user"></span>&nbsp;<span class="message"></span>
          <span class="time"></span>
        </li>
      </ul>
    </div>
    <div id="input">
      <form><input type="text" id="message" /></form>
    </div>
  </div>
</body>
</html>
