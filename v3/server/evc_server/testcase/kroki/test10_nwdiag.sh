curl http://evc.re.kr:28010/nwdiag/svg --data-binary '@network.nwdiag' > ../../web/tmp/t10.html
curl http://evc.re.kr:28010/nwdiag/svg --data-binary '@network.nwdiag'

curl http://evc.re.kr:28010/nwdiag/svg --data-binary '@cluster1.nwdiag' > ../../web/tmp/t10a.html
curl http://evc.re.kr:28010/nwdiag/svg --data-binary '@cluster1.nwdiag'

curl http://evc.re.kr:28010/nwdiag/svg --data-binary '@cluster2.nwdiag' > ../../web/tmp/t10b.html
curl http://evc.re.kr:28010/nwdiag/svg --data-binary '@cluster2.nwdiag'
