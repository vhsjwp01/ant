%define __os_install_post %{nil}
%define uek %( uname -r | egrep -i uek | wc -l | awk '{print $1}' )
%define rpm_arch %( uname -p )
%define rpm_author Jason W. Plummer
%define rpm_author_email jason.plummer@ingramcontent.com
%define distro_id %( lsb_release -is )
%define distro_ver %( lsb_release -rs )
%define distro_major_ver %( echo "%{distro_ver}" | awk -F'.' '{print $1}' )
%define source_url http://archive.apache.org/dist/ant/binaries/

Summary: The Apache ANT builder
Name: icg-ant
Release: 1.EL%{distro_major_ver}
License: GNU
Group: Development/Compiler
BuildRoot: %{_tmppath}/%{name}-root

# This does a scrape of the %{source_url} looking for the version specified
%define ant_archive_name apache-ant
%define ant_version 1.9.4
%define ant_version_url %( elinks -dump %{source_url} | egrep "%{source_url}.*%{ant_archive_name}\-%{ant_version}\-bin.tar.gz$" | sort | tail -1 | awk '{print $NF}' )

Version: %{ant_version}
URL: %{ant_version_url}

# This block handles Oracle Linux UEK .vs. EL BuildRequires
#%if %{uek}
#BuildRequires: kernel-uek-devel, kernel-uek-headers
#%else
#BuildRequires: kernel-devel, kernel-headers
#%endif
# These BuildRequires can be found in EPEL

# These Requires can be found in Base
Requires: curl >= 0
Requires: gzip >= 0
Requires: tar  >= 0

%define install_dir /usr/share

# Define our variables here
Source0: %{url}

%description
Apache Ant is a Java library and command-line tool that help building software

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{install_dir}
# Populate %{buildroot}
cd %{buildroot}%{install_dir} && curl -O %{url}
if [ -e "%{ant_archive_name}-%{ant_version}-bin.tar.gz" ]; then
    zcat "%{ant_archive_name}-%{ant_version}-bin.tar.gz" | tar xvf -
fi
if [ -d "%{ant_archive_name}-%{ant_version}" ]; then
    rm -f "%{ant_archive_name}-%{ant_version}-bin.tar.gz"
fi
# Build packaging manifest
rm -rf /tmp/MANIFEST.%{name}* > /dev/null 2>&1
echo '%defattr(-,root,root)' > /tmp/MANIFEST.%{name}
chown -R root:root %{buildroot} > /dev/null 2>&1
cd %{buildroot}
find . -depth -type d -exec chmod 755 {} \;
find . -depth -type f -exec chmod 644 {} \;
for i in `find . -depth -type f | sed -e 's/\ /zzqc/g'` ; do
    filename=`echo "${i}" | sed -e 's/zzqc/\ /g'`
    eval is_exe=`file "${filename}" | egrep -i "executable" | wc -l | awk '{print $1}'`
    if [ "${is_exe}" -gt 0 ]; then
        chmod 555 "${filename}"
    fi
done
find . -type f -or -type l | sed -e 's/\ /zzqc/' -e 's/^.//' -e '/^$/d' > /tmp/MANIFEST.%{name}.tmp
for i in `awk '{print $0}' /tmp/MANIFEST.%{name}.tmp` ; do
    filename=`echo "${i}" | sed -e 's/zzqc/\ /g'`
    dir=`dirname "${filename}"`
    echo "${dir}/*"
done | sort -u >> /tmp/MANIFEST.%{name}
# Clean up what we can now and allow overwrite later
rm -f /tmp/MANIFEST.%{name}.tmp
chmod 666 /tmp/MANIFEST.%{name}

%files -f /tmp/MANIFEST.%{name}

%changelog
%define today %( date +%a" "%b" "%d" "%Y )
* %{today} %{rpm_author} <%{rpm_author_email}>
- built version %{version} for %{distro_id} %{distro_ver}

