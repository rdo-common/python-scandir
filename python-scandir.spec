%global pkgname scandir

%if 0%{?fedora} > 12
%global with_python3 1
%endif

Name:           python-%{pkgname}
Version:        1.1
Release:        1%{?dist}
Summary:        A better directory iterator and faster os.walk() for Python
URL:            https://github.com/benhoyt/scandir
Source:         %{url}/archive/v%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
License:        BSD

BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
scandir() is a directory iteration function like os.listdir(), except that
instead of returning a list of bare filenames, it yields DirEntry objects that
include file type and stat information along with the name. Using scandir()
increases the speed of os.walk() by 2-20 times (depending on the platform and
file system) by avoiding unnecessary calls to os.stat() in most cases.
scandir is included in the Python 3.5+ standard library.

%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        A better directory iterator and faster os.walk() for Python

%description -n python3-%{pkgname}
scandir() is a directory iteration function like os.listdir(), except that
instead of returning a list of bare filenames, it yields DirEntry objects that
include file type and stat information along with the name. Using scandir()
increases the speed of os.walk() by 2-20 times (depending on the platform and
file system) by avoiding unnecessary calls to os.stat() in most cases.
scandir is included in the Python 3.5+ standard library.
%endif

%prep
%setup -q -n %{pkgname}-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif

%install
%{__python} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%check
echo %{python3_sitearch}
# Tests fail if unicode is not supported
LANG=en_US.utf8
%{__python} test/run_tests.py
rm -rf test/testdir
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} test/run_tests.py
rm -rf test/testdir
popd
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README* test benchmark.py
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README* test benchmark.py
%exclude %dir %{python3_sitearch}/__pycache__
%{python3_sitearch}/*
%endif

%changelog
* Wed Jul 22 2015 Avram Lubkin <avram@rockhopper.net> - 1.1-1
- Initial package.

