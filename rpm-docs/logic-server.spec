Name:           logic-server
Version:        1
Release:        0
Summary:        The logic service for Trading App

License:        GPL
URL:            https://github.com/ansh-shmyg/logic-srv
Source0:        logic-server-1.0.tar.gz

#BuildRequires:  
Requires:       python36
#BuildArch:      noarch
%description
The service for devops team traiding app.

%global	username app-logic

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
useradd -r -g %{username} -M -s /sbin/nologin \
-c "Account to own and run %{username}" %{username}
exit

%prep
%setup -q
%build
%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/opt/%{username}
install -m 0750 logic_server.py $RPM_BUILD_ROOT/opt/%{username}/logic_server.py

%files
%defattr(0750, %{username}, %{username}, 0755)
/opt/%{username}
/opt/%{username}/logic_server.py

%changelog
* Tue Jul 16 2019 Andrii Shmyhovskiy 1.0.0
  - Build simple package
