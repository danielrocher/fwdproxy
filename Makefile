
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
	useradd -r -s /bin/false fwdproxyd

install_program:
	mkdir -p /opt/fwdproxyd/
	cp -r * /opt/fwdproxyd/
	chown root:fwdproxyd /opt/fwdproxyd -R
	find /opt/fwdproxyd/ -type d -exec chmod u=rwx,g=rx,o= {} \;
	find /opt/fwdproxyd/ -type f -exec chmod u=rw,g=r,o= {} \;
	find /opt/fwdproxyd/ -type f -name '*.py' -exec chmod u=rwx,g=rx,o= {} \;
	chmod u=rwx,g=rx,o= /opt/fwdproxyd/fwdproxyd
	chmod o+rx /opt

install_configuration:
	mkdir -p /etc/fwdproxyd
	cp fwdproxyd.conf /etc/fwdproxyd/
	chown root:fwdproxyd /etc/fwdproxyd -R
	chmod u=rwx,g=rx,o= /etc/fwdproxyd
	chmod u=rw,g=r,o= /etc/fwdproxyd/*

install_service:
	cp fwdproxyd.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable fwdproxyd.service
	systemctl start fwdproxyd.service


