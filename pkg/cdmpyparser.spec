%define name cdmpyparser
%define release 1
%define version %{getenv:version}

Summary: Fast and comprehensive parser of the Python language
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
License: GPLv3+
Group: Development/Libraries
URL: https://github.com/SergeySatskiy/codimension

Requires: python

BuildRequires: python-devel
BuildRequires: gcc
BuildRequires: gcc-c++
Source: https://github.com/SergeySatskiy/codimension/releases/%{name}-%{version}.tar.gz

%description
Written as a part of the Codimension project, this parser aims at
pulling the most data from Python sources while exceeding the
speed of existing parsers.

%prep
%setup -q -n %{name}-%{version}

%build
make

%install
python setup.py install --root=${RPM_BUILD_ROOT} --record=INSTALLED_FILES

%check
make check

%files -f INSTALLED_FILES
%doc AUTHORS LICENSE ChangeLog README.md
%{python_sitearch}/cdmbriefparser.pyo

%changelog
* Sat Jan 16 2016 Sergey Fukanchik <fukanchik@gmail.com> - 2.0.0
- Initial version of the package.

