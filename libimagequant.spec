# TODO:
# - finish java (create .jar, install)
# - build C#, rust bindings
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	openmp		# OpenMP support
%bcond_with	sse		# SSE instructions
%bcond_with	java		# Java bindings [TODO: finish]
#
%ifarch pentium3 pentium4 %{x8664} x32
%define	with_sse	1
%endif
Summary:	Image Quantization library
Summary(pl.UTF-8):	Biblioteka do kwantyzacji obrazów
Name:		libimagequant
Version:	2.12.5
Release:	1
# some original code was on MIT-like license
License:	GPL v3+ with MIT parts or commercial
Group:		Libraries
#Source0Download: https://github.com/ImageOptim/libimagequant/releases
Source0:	https://github.com/ImageOptim/libimagequant/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	de703ea6cd650c332f1ba2a23b234294
Patch0:		%{name}-shared.patch
URL:		https://pngquant.org/lib/
%{?with_openmp:BuildRequires:	gcc >= 6:4.2}
%{?with_java:BuildRequires:	jdk}
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Small, portable C library for high-quality conversion of RGBA images
to 8-bit indexed-color (palette) images.

%description -l pl.UTF-8
Mała, przenośna biblioteka C do wysokiej jakości konwersji obrazów
RGBA do obrazów 8-bitowych z indeksowanymi kolorami (paletą).

%package devel
Summary:	Header files for libimagequant library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libimagequant
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libimagequant library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libimagequant.

%package static
Summary:	Static libimagequant library
Summary(pl.UTF-8):	Statyczna biblioteka libimagequant
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libimagequant library.

%description static -l pl.UTF-8
Statyczna biblioteka libimagequant.

%prep
%setup -q
%patch0 -p1

%build
# not autoconf configure
./configure \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	%{__enable_disable sse} \
	%{?with_openmp:--with-openmp}

%{__make} shared %{?with_static_libs:static}

%if %{with java}
%{__make} java \
	CLASSPATH=.
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
cp -p libimagequant.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYRIGHT README.md
%attr(755,root,root) %{_libdir}/libimagequant.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libimagequant.so
%{_includedir}/libimagequant.h
%{_pkgconfigdir}/imagequant.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libimagequant.a
%endif
