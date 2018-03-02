
build:
	py3compile include/
	py3compile fwdproxyd unit_test.py

clean:
	find . -name \*.pyc -type f -delete
	find . -name __pycache__ -type d -delete

install: build create_user install_configuration install_program install_service

uninstall:
	systemctl stop fwdproxyd.service
	systemctl disable fwdproxyd.service
	rm /etc/systemd/system/fwdproxyd.service
	rm -rf /opt/fwdproxyd
	rm -rf /etc/fwdproxyd
	userdel -r fwdproxyd

create_user:
	useradd -r fwdproxyd

install_program:
	mkdir -p /opt/fwdproxyd/
	cp -Pr * /opt/fwdproxyd/
	chown fwdproxyd:fwdproxyd /opt/fwdproxyd -R
	chmod o-rwx /opt/fwdproxyd/ -R
	chmod o+rx /opt

install_configuration:
	mkdir -p /etc/fwdproxyd
	cp fwdproxyd.conf /etc/fwdproxyd/
	chown fwdproxyd:fwdproxyd /etc/fwdproxyd

install_service:
	cp fwdproxyd.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable fwdproxyd.service
	systemctl start fwdproxyd.service


