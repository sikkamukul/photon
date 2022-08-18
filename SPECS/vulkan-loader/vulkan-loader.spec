Name:           vulkan-loader
Version:        1.3.230
Release:        1%{?dist}
Summary:        Vulkan ICD desktop loader
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Loader

Source0:        https://github.com/KhronosGroup/Vulkan-Loader/archive/refs/tags/Vulkan-Loader-%{version}.tar.gz
%define sha512  Vulkan-Loader-%{version}.tar.gz=3d7a07d01dc76d474661b2771b9ea522075d3975832db63309169cea726c51fa35e02d79d7183adc552ef70831190dac6272fd5715c12ba9ceee9c048f565f70

BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  vulkan-headers
BuildRequires:  libxml2-devel
BuildRequires:  wayland-devel
BuildRequires:  libwayland-client
BuildRequires:  libwayland-cursor
BuildRequires:  libwayland-server
BuildRequires:  libwayland-egl
BuildRequires:  libxcb-devel
BuildRequires:  libX11-devel
BuildRequires:  libXrandr-devel

Requires:       vulkan-headers
Requires:       mesa-vulkan-drivers
Provides:       vulkan = %{version}-%{release}
Provides:       vulkan-filesystem = %{version}-%{release}

%description
This project provides the Khronos official Vulkan ICD desktop
loader for Windows, Linux, and MacOS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       vulkan-headers
Provides:       vulkan-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n Vulkan-Loader-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release \
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
        -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir}

%cmake_build

%install
%cmake_install

# create the filesystem
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/{explicit,implicit}_layer.d/ \
         %{buildroot}%{_datadir}/vulkan/{explicit,implicit}_layer.d/ \
         %{buildroot}{%{_sysconfdir},%{_datadir}}/vulkan/icd.d/ \
         %{buildroot}%{_libdir}

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE.txt
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/vulkan/
%dir %{_sysconfdir}/vulkan/explicit_layer.d/
%dir %{_sysconfdir}/vulkan/icd.d/
%dir %{_sysconfdir}/vulkan/implicit_layer.d/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/vulkan/explicit_layer.d/
%dir %{_datadir}/vulkan/icd.d/
%dir %{_datadir}/vulkan/implicit_layer.d/
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/vulkan.pc
%{_libdir}/*.so

%changelog
*   Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.230-1
-   Automatic Version Bump
*   Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.216.0-2
-   Bump version as a part of mesa upgrade
*   Mon Jun 13 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.216.0-1
-   Initial version