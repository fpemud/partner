PACKAGE_VERSION=0.0.1
prefix=/usr

all:

install:
	install -d -m 0755 "$(DESTDIR)/$(prefix)/sbin"
	install -m 0755 partner-daemon "$(DESTDIR)/$(prefix)/sbin"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/partner"
	cp -r lib/* "$(DESTDIR)/$(prefix)/lib/partner"
	find "$(DESTDIR)/$(prefix)/lib/partner" -path "$(DESTDIR)/$(prefix)/lib/partner/plugins" -prune -o -type f | xargs chmod 644
	find "$(DESTDIR)/$(prefix)/lib/partner" -path "$(DESTDIR)/$(prefix)/lib/partner/plugins" -prune -o -type d | xargs chmod 755

	install -d -m 0755 "$(DESTDIR)/etc/partner"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/systemd/system"
	install -m 0644 data/system/partner.service "$(DESTDIR)/$(prefix)/lib/systemd/system"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/systemd/user"
	install -m 0644 data/user/partner.service "$(DESTDIR)/$(prefix)/lib/systemd/user"

	install -d -m 0755 "$(DESTDIR)/etc/dbus-1/system.d"
	install -m 0644 data/org.fpemud.Partner.conf "$(DESTDIR)/etc/dbus-1/system.d"

uninstall:
	rm -f "$(DESTDIR)/$(prefix)/sbin/partner"
	rm -f "$(DESTDIR)/$(prefix)/lib/systemd/system/partner.service"
	rm -f "$(DESTDIR)/$(prefix)/lib/systemd/user/partner.service"
	rm -f "$(DESTDIR)/$(prefix)/etc/dbus-1/system.d/org.fpemud.WRT.conf"
	rm -rf "$(DESTDIR)/$(prefix)/lib/partner"
	rm -rf "$(DESTDIR)/etc/partner"

.PHONY: all install uninstall
