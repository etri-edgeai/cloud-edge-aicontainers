from decenter.ai.flask import msghandler

@msghandler.route('/test')
def test():
    return 'custom msg handler test page'
