%define debug_package %{nil}

Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        7.0.100
Release:        rc1.1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools

# Download source tarball from the links provided in:
# https://github.com/dotnet/core/tree/main/release-notes
#
# For example:
# https://github.com/dotnet/core/blob/main/release-notes/6.0/6.0.0/6.0.0.md
# https://download.visualstudio.microsoft.com/download/pr/17b6759f-1af0-41bc-ab12-209ba0377779/e8d02195dbf1434b940e0f05ae086453/dotnet-sdk-6.0.100-linux-x64.tar.gz
Source0: %{name}-%{version}-rc1-linux-x64.tar.gz
%define sha512 %{name}=7ecebf284bd1546e1575b9561f4e64bbb8d69680a7bbda6f06ff6fbf687d3a6c653b0e6a6c569241455c6f83620f0ddbe193ca5cd52384ac062c8565dd22b859

BuildArch:      x86_64

Requires:       dotnet-runtime >= 7.0.0
Requires:       icu >= 70.1

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -c %{name}-%{version} -p1

%build

%install
ver="7.0.100-rc.1.22431.12"
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk %{buildroot}%{_docdir}/%{name}-%{version}
cp -r sdk/${ver} %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-sdk-%{version}

%files
%defattr(-,root,root,0755)
%{_libdir}/*
%{_docdir}/*

%changelog
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.100-rc1.1
- Bump version as a part of icu upgrade
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.100-rc1
- Upgrade to v7.0.100-rc1
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 6.0.100-2
- Release bump to build with icu-70.1
* Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 6.0.100-1
- Upgrade to version 6.0.100
* Tue Oct 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0.402-1
- Upgrade to version 5.0.402
* Tue Mar 9 2021 Shreyas B. <shreyasb@vmware.com> 5.0.103-1
- upgrade to version 5.0.103
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.201-1
- Automatic Version Bump
* Thu Nov 07 2019 Shreyas B. <shreyasb@vmware.com> 2.1.509-1
- upgraded to version 2.1.509
* Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.1.403-1
- upgraded to version 2.1.403
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
- Initial build for photon