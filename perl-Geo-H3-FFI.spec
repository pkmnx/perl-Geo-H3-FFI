Name:           perl-Geo-H3-FFI
Version:        0.01
Release:        1%{?dist}
Summary:        Perl binding to call H3 functions
License:        mit
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Geo-H3-FFI/
Source0:        http://www.cpan.org/modules/by-module/Geo/Geo-H3-FFI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Perl binding to call H3 functions

%prep
%setup -q -n Geo-H3-FFI-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes META.json README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue May 18 2021 Michael R. Davis <mrdvt@cpan.org> 0.01-1
- Specfile autogenerated by cpanspec 1.78.
