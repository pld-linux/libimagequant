# TODO:
# - finish java (create .jar, install)
# - build C# bindings, rust crates
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	sse		# SSE instructions
%bcond_with	java		# Java bindings [TODO: finish]
#
%ifarch pentium3 pentium4 %{x8664} x32
%define	with_sse	1
%endif
Summary:	Image Quantization library
Summary(pl.UTF-8):	Biblioteka do kwantyzacji obrazów
Name:		libimagequant
Version:	4.3.0
Release:	1
# some original code was on MIT-like license
License:	GPL v3+ with MIT parts or commercial
Group:		Libraries
#Source0Download: https://github.com/ImageOptim/libimagequant/tags
Source0:	https://github.com/ImageOptim/libimagequant/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c5290deecd9a1a7d115a823435dbd0a2
Source1:	%{name}-%{version}-vendor.tar.xz
# Source1-md5:	1e5c3a19b4c5099e151eb4fcfed4e96b
URL:		https://pngquant.org/lib/
BuildRequires:	cargo
BuildRequires:	cargo-c
%{?with_java:BuildRequires:	jdk}
BuildRequires:	rpmbuild(macros) >= 2.012
BuildRequires:	rust >= 1.70
ExclusiveArch:	%{x8664} %{ix86} x32 aarch64 armv6hl armv7hl armv7hnl
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
%setup -q -b1

export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

cd imagequant-sys
cargo -v cbuild --offline --release --target %{rust_target} \
        --prefix %{_prefix} \
        --libdir %{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

cd imagequant-sys
cargo -v cinstall --frozen --release --target %{rust_target} \
	--destdir $RPM_BUILD_ROOT \
	--prefix %{_prefix} \
	--includedir %{_includedir} \
	--libdir %{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYRIGHT README.md
%attr(755,root,root) %{_libdir}/libimagequant.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimagequant.so.0.4

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
