%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%global realname v
%global upstream vlang
%global gitbase  https://github.com

Summary:  The V Programming Language
Name:     vlang
Version:  0.4.3
Release:  1
License:  MIT
Group:    Development/Other
Url:      https://vlang.io
Source0:  %{gitbase}/%{upstream}/%{realname}/archive/refs/tags/%{version}.tar.gz
Source1:  vc_%{version}.tar.xz
Source2:  vmod_markdown_0c28013.tar.xz
Patch0:   builtin-force-dynamic-gc-lib.patch
Patch1:   json-support-system-cJSON-library-through-pkgconfig.patch
Patch2:   compress-support-system-miniz-library-through-pkgconfig.patch
Patch3:   vlib-prefer-openssl-over-mbedtls.patch
Patch4:   time-fix-off-by-1-error-in-must_be_valid_three_letter_month.patch

BuildRequires: atomic-devel
BuildRequires: git-core
BuildRequires: pkgconfig(bdw-gc)
BuildRequires: pkgconfig(libcjson)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(mariadb)
BuildRequires: pkgconfig(miniz)
BuildRequires: pkgconfig(opengl)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xi)

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
shopt -s extglob
rm -r thirdparty/!(fontstash|sokol|stb_image|stdatomic)/

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
VTEST_JUST_ESSENTIAL=1 ./v test-self

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
