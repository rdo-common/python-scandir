%global pkgname scandir

%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?epel} > 6
%global with_python3 1
%endif

# Rename to python2-configparser after Fedora 23
%if 0%{?fedora} > 23
  %global with_p2subpkg 1
%endif

# __python2 macro doesn't exist for el6
%if 0%{?el6}
  %define __python2 %{__python}
  %define python2_sitearch %{python_sitearch}
%endif

Name:           python-%{pkgname}
Version:        1.2
Release:        4%{?dist}
Summary:        A better directory iterator and faster os.walk() for Python
URL:            https://github.com/benhoyt/scandir
Source:         %{url}/archive/v%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
License:        BSD
BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
%endif

%description
scandir() is a directory iteration function like os.listdir(), except that
instead of returning a list of bare filenames, it yields DirEntry objects that
include file type and stat information along with the name. Using scandir()
increases the speed of os.walk() by 2-20 times (depending on the platform and
file system) by avoiding unnecessary calls to os.stat() in most cases.
scandir is included in the Python 3.5+ standard library.

%if 0%{?with_p2subpkg}
%package -n python2-%{pkgname}
Summary:        A better directory iterator and faster os.walk() for Python
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
scandir() is a directory iteration function like os.listdir(), except that
instead of returning a list of bare filenames, it yields DirEntry objects that
include file type and stat information along with the name. Using scandir()
increases the speed of os.walk() by 2-20 times (depending on the platform and
file system) by avoiding unnecessary calls to os.stat() in most cases.
scandir is included in the Python 3.5+ standard library.
%else
Provides:       python2-%{pkgname} = %{version}-%{release}
%endif

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{pkgname}
Summary:        A better directory iterator and faster os.walk() for Python
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}

%description -n python%{python3_pkgversion}-%{pkgname}
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
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%check
echo %{python3_sitearch}
# Tests fail if unicode is not supported
LANG=en_US.utf8
%{__python2} test/run_tests.py
rm -rf test/testdir
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} test/run_tests.py
rm -rf test/testdir
popd
%endif

# For Fedora > 23 builds
%if 0%{?with_p2subpkg}
%files -n python2-%{pkgname}
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README* test benchmark.py
%{python2_sitearch}/*
%attr(755,root,root) %{python2_sitearch}/*.so
%else
%files
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README* test benchmark.py
%{python2_sitearch}/*
%attr(755,root,root) %{python2_sitearch}/*.so
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{pkgname}
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README* test benchmark.py
%exclude %dir %{python3_sitearch}/__pycache__
%{python3_sitearch}/*
%attr(755,root,root) %{python3_sitearch}/*.so
%endif

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 20 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.2-3
- Build Python3 package for el7+

* Tue Jan 19 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.2-2
- Fixed typos and logic in spec file

* Mon Jan 18 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.2-1
- Updated to version 1.2
- Use python2 macros instead of bare python macros
- Changed Python2 package name to python2-scandir for Fedora 24+
- Use python3_pkgversion for package names

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jul 22 2015 Avram Lubkin <aviso@fedoraproject.org> - 1.1-1
- Initial package.

