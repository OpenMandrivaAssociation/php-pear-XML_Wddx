%define		_class		XML
%define		_subclass	Wddx
%define		upstream_name	%{_class}_%{_subclass}

Name:		php-pear-%{upstream_name}
Version:	1.0.1
Release:	%mkrel 11
Summary:	Wddx pretty serializer and deserializer
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/XML_Wddx/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
XML_Wddx does 2 things:
- a drop in replacement for the XML_Wddx extension (if it's not built
  in)
- produce an editable wddx file (with indenting etc.) and uses CDATA,
  rather than char tags

This package contains 2 static method:
- XML_Wddx:serialize(\$value)
- XML_Wddx:deserialize(\$value)

And should be 90% compatible with wddx_deserialize(), and the
deserializer will use wddx_deserialize if it is built in.

No support for recordsets is available at present in the PHP version
of the deserializer.

%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml


