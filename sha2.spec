#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	SHA Implementation Library
Name:		sha2
Version:	1.0.1
Release:	1
License:	BSD
URL:		http://www.aarongifford.com/computers/sha.html
Source0:	http://www.aarongifford.com/computers/%{name}-%{version}.tgz
# Source0-md5:	5c050ef4edb9d5198e7d57e759c4996f
Source1:	Makefile
Group:		Libraries
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The library implements the SHA-256, SHA-384, and SHA-512 hash
algorithms. The interface is similar to the interface to SHA-1 found
in the OpenSSL library.

sha2 is a simple program that accepts input from either STDIN or reads
one or more files specified on the command line, and then generates
the specified hash (either SHA-256, SHA-384, SHA-512, or any
combination thereof, including all three at once).

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	devel
This package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q
cp -p %{SOURCE1} Makefile

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%if %{with tests}
LD_PRELOAD=./libsha2.so ./sha2test.pl
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir} \
	BINDIR=%{_bindir} \
	OPTFLAGS="%{optflags}"

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/sha2
%attr(755,root,root) %{_bindir}/sha2speed
%attr(755,root,root,) %{_libdir}/libsha2.so.*.*.*
%ghost %{_libdir}/libsha2.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/sha2.h
%{_libdir}/libsha2.so
