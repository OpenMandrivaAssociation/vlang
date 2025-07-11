%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%global realname v
%global upstream vlang
%global gitbase  https://github.com

Summary:  The V Programming Language
Name:     vlang
Version:  0.4.11
Release:  2
License:  MIT
Group:    Development/Other
Url:      https://vlang.io
Source0:  %{gitbase}/%{upstream}/%{realname}/archive/refs/tags/%{version}.tar.gz
Source1:  vc_%{version}.tar.zst
Source2:  vmod_markdown_5a1c9d8.tar.zst
Patch0:   builtin-force-dynamic-gc-lib.patch
Patch1:   compress-support-system-zstd-library-through-pkgconfig.patch
Patch2:   json-support-system-cJSON-library-through-pkgconfig.patch
Patch3:   net-support-system-mbedtls-library-through-pkgconfig.patch
Patch4:   vlib-prefer-openssl-over-mbedtls.patch
Patch5:   os-don-t-resolve-symlinks-in-find_abs_path_of_execut.patch
Patch6:   cgen-only-run-freestanding_module_import-on-amd64.patch

BuildRequires: atomic-devel
BuildRequires: git-core
BuildRequires: glibc-debuginfo
BuildRequires: valgrind
BuildRequires: pkgconfig(bdw-gc)
BuildRequires: pkgconfig(libcjson)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(mariadb)
BuildRequires: pkgconfig(mbedtls)
BuildRequires: pkgconfig(opengl)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xrandr)

Requires: pkgconfig(bdw-gc)

Provides: v = %{version}-%{release}

%description
Simple, fast, safe, compiled. For developing maintainable software.

%prep
%autosetup -p 1 -n %{realname}-%{version}
%setup -T -D -a 1 -q -n %{realname}-%{version}

# Required for the "build-tools" command.
%setup -T -D -a 2 -q -n %{realname}-%{version}

# Remove as many bundled dependencies as possible.
# Required:
# - "fontstash": font processing headers.
# - "sokol": video and audio rendering.
# - "stb_image": stb with a few modifications, mostly wrappers.
# - "stdatomic": cross-platform wrappers for atomic stuff.
# - "zip": miniz + wrapper.
shopt -s extglob
rm -r thirdparty/!(fontstash|sokol|stb_image|stdatomic|zip)/

mkdir -p ~/.vmodules
mv -vn markdown-master ~/.vmodules/markdown

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_libexecdir}/%{name}

%build
%set_build_flags
export VFLAGS="-prod"

$CC $CFLAGS -std=gnu99 -w -o tmp_1 v.c -lm -lpthread $LDFLAGS
./tmp_1 -no-parallel -o tmp_2 $VFLAGS cmd/v
./tmp_2 -o v $VFLAGS cmd/v

./v build-tools

%check
./v test-self

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libexecdir}/%{name}
cp -a %{realname} %{realname}.mod %{realname}lib cmd thirdparty %{buildroot}%{_libexecdir}/%{name}/
ln -s %{_libexecdir}/%{name}/%{realname} %{buildroot}%{_bindir}/%{realname}
touch %{buildroot}%{_libexecdir}/%{name}/cmd/tools/.disable_autorecompilation

%files
%doc doc/* CHANGELOG.md
%license LICENSE

%{_bindir}/%{realname}
%{_libexecdir}/%{name}
