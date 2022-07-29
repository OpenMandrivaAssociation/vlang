%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%global realname v
%global upstream vlang
%global gitbase  https://github.com

Summary:  The V Programming Language
Name:     vlang
Version:  0.3
Release:  1
License:  MIT
Group:    Development/Other
Url:      https://vlang.io
Source0:  %{gitbase}/%{upstream}/%{realname}/archive/refs/tags/%{version}.tar.gz
Source1:  vc_%{version}.tar.xz

BuildRequires: devel(libatomic)
BuildRequires: pkgconfig(bdw-gc)
BuildRequires: pkgconfig(libssl)
BuildRequires: git-core

Provides: v = %{version}-%{release}

%description
Simple, fast, safe, compiled. For developing maintainable software.

%prep
%setup -q -n %{realname}-%{version}
%setup -T -D -a 1 -q -n %{realname}-%{version}

git clone %{gitbase}/%{upstream}/markdown.git ~/.vmodules/markdown

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_libexecdir}/%{name}

%build
%set_build_flags
export VFLAGS="-prod -d dynamic_boehm"

$CC $CFLAGS -std=gnu99 -w -o tmp_1 v.c -lm -lpthread $LDFLAGS
./tmp_1 -no-parallel -o tmp_2 $VFLAGS cmd/v
./tmp_2 -o v $VFLAGS cmd/v

./v build-tools
./v test-all

%install
cp -a %{realname} %{realname}.mod %{realname}lib cmd %{buildroot}%{_libexecdir}/%{name}/
ln -s %{_libexecdir}/%{name}/%{realname} %{buildroot}%{_bindir}/%{realname}
touch %{buildroot}%{_libexecdir}/%{name}/cmd/tools/.disable_autorecompilation

%files
%doc doc/* CHANGELOG.md
%license LICENSE

%{_bindir}/%{realname}
%{_libexecdir}/%{name}
