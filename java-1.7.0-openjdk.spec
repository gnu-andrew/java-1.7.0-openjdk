# If debug is 1, OpenJDK is built with all debug info present.
%global debug 0

%global icedtea_version 2.4.2
%global hg_tag icedtea-{icedtea_version}

%global aarch64			aarch64 arm64 armv8
%global multilib_arches %{power64} sparc64 x86_64 %{aarch64}
%global jit_arches		%{ix86} x86_64 sparcv9 sparc64

#links are set forcibly, f19 32b fix
%global graceful_links 0

%ifarch x86_64
%global archbuild amd64
%global archinstall amd64
%endif
%ifarch ppc
%global archbuild ppc
%global archinstall ppc
%global archdef PPC
%endif
%ifarch %{power64}
%global archbuild ppc64
%global archinstall ppc64
%global archdef PPC
%endif
%ifarch %{ix86}
%global archbuild i586
%global archinstall i386
%endif
%ifarch ia64
%global archbuild ia64
%global archinstall ia64
%endif
%ifarch s390
%global archbuild s390
%global archinstall s390
%global archdef S390
%endif
%ifarch s390x
%global archbuild s390x
%global archinstall s390x
%global archdef S390
%endif
%ifarch %{arm}
%global archbuild arm
%global archinstall arm
%global archdef ARM
%endif
%ifarch %{aarch64}
%global archbuild aarch64
%global archinstall aarch64
%global archdef AARCH64
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archbuild sparc
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archbuild sparcv9
%global archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%global archbuild %{_arch}
%global archinstall %{_arch}
%endif

%if %{debug}
%global debugbuild debug_build
%else
%global debugbuild %{nil}
%endif

%global buildoutputdir openjdk/build/linux-%{archbuild}

%global with_pulseaudio 1

%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

# Hard-code libdir on 64-bit architectures to make the 64-bit JDK
# simply be another alternative.
%ifarch %{multilib_arches}
%global syslibdir       %{_prefix}/lib64
%global _libdir         %{_prefix}/lib
%else
%global syslibdir       %{_libdir}
%endif

# Standard JPackage naming and versioning defines.
%global origin          openjdk
%global updatever        40
#Fedora have an bogus 60 instead of updatever. Fix when updatever>=60 in version:
%global buildver        60
# Keep priority on 6digits in case updatever>9
%global priority        1700%{updatever}
%global javaver         1.7.0

%global sdkdir          %{uniquesuffix}
%global jrelnk          jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}

%global jredir          %{sdkdir}/jre
%global sdkbindir       %{_jvmdir}/%{sdkdir}/bin
%global jrebindir       %{_jvmdir}/%{jredir}/bin
%global jvmjardir       %{_jvmjardir}/%{uniquesuffix}

%global fullversion     %{name}-%{version}-%{release}

%global uniquesuffix          %{fullversion}.%{_arch}
#we can copy the javadoc to not arched dir, or made it not noarch
%global uniquejavadocdir       %{fullversion}

%global statuscheck		status is auto
%global linkcheck		link currently points to

%ifarch %{jit_arches}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{_build_cpu}
%endif

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.60
Release: %{icedtea_version}.5%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL:      http://openjdk.java.net/

#head
#REPO=http://icedtea.classpath.org/hg/icedtea7-forest
#current release
#REPO=http://icedtea.classpath.org/hg/release/icedtea7-forest-2.4
# hg clone $REPO/ openjdk -r %{hg_tag}
# hg clone $REPO/corba/ openjdk/corba -r %{hg_tag}
# hg clone $REPO/hotspot/ openjdk/hotspot -r %{hg_tag}
# hg clone $REPO/jaxp/ openjdk/jaxp -r %{hg_tag}
# hg clone $REPO/jaxws/ openjdk/jaxws -r %{hg_tag}
# hg clone $REPO/jdk/ openjdk/jdk -r %{hg_tag}
# hg clone $REPO/langtools/ openjdk/langtools -r %{hg_tag}
# find openjdk -name ".hg" -exec rm -rf '{}' \;
# sh /git/java-1.7.0-openjdk/fX/fsg.sh
# tar cJf openjdk-icedtea-%{icedtea_version}.tar.xz openjdk
Source0:  openjdk-icedtea-%{icedtea_version}.tar.xz

# README file
# This source is under maintainer's/java-team's control
Source2:  README.src

# Sources 6-12 are taken from hg clone http://icedtea.classpath.org/hg/icedtea7
# Unless said differently, there is directory with required sources which should be enough to pack/rename

# Class rewrite to rewrite rhino hierarchy
Source5: class-rewriter.tar.gz

# Systemtap tapsets. Zipped up to keep it small.
Source6: systemtap-tapset.tar.gz

# .desktop files. 
Source7:  policytool.desktop
Source77: jconsole.desktop

# nss configuration file
Source8: nss.cfg

# FIXME: Taken from IcedTea snapshot 877ad5f00f69, but needs to be moved out
# hg clone -r 877ad5f00f69 http://icedtea.classpath.org/hg/icedtea7
Source9: pulseaudio.tar.gz

# Removed libraries that we link instead
Source10: remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source11: TestCryptoLevel.java

# RPM/distribution specific patches

# Allow TCK to pass with access bridge wired in
Patch1:   java-1.7.0-openjdk-java-access-bridge-tck.patch

# Disable access to access-bridge packages by untrusted apps
Patch3:   java-1.7.0-openjdk-java-access-bridge-security.patch

# Ignore AWTError when assistive technologies are loaded 
Patch4:   java-1.7.0-openjdk-accessible-toolkit.patch

# Build docs even in debug
Patch5:   java-1.7.0-openjdk-debugdocs.patch

# Add debuginfo where missing
Patch6:   %{name}-debuginfo.patch

#
# OpenJDK specific patches
#

# Add rhino support
Patch100: rhino.patch

# Type fixing for s390
Patch101: zero-s8024914.patch
Patch102: zero-size_t.patch

# Patch for PPC/PPC64
Patch104: %{name}-ppc-zero-jdk.patch
Patch105: %{name}-ppc-zero-hotspot.patch

Patch106: %{name}-freetype-check-fix.patch

# Zero fixes
Patch110: zero-entry_frame_call_wrapper.patch
Patch111: zero-zero_build.patch
Patch112: zero-gcdrainstacktargetsize.patch

# allow to create hs_pid.log in tmp (in 700 permissions) if working directory is unwritable
Patch200: abrt_friendly_hs_log_jdk7.patch

#
# Optional component packages
#

# Make the ALSA based mixer the default when building with the pulseaudio based
# mixer
Patch300: pulse-soundproperties.patch

#Workaround RH902004
Patch402: gstackbounds.patch
Patch403: PStack-808293.patch
Patch404: RH661505-toBeReverted.patch
# End of tmp patches

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: alsa-lib-devel
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: giflib-devel
BuildRequires: lcms2-devel >= 2.5
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXp-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: wget
BuildRequires: libxslt
BuildRequires: xorg-x11-proto-devel
BuildRequires: mercurial
BuildRequires: ant
BuildRequires: ant-nodeps
BuildRequires: libXinerama-devel
BuildRequires: rhino
BuildRequires: redhat-lsb
BuildRequires: zip
BuildRequires: fontconfig
BuildRequires: xorg-x11-fonts-Type1
BuildRequires: zlib > 1.2.3-6
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: fontconfig
BuildRequires: at-spi-devel
BuildRequires: gawk
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: xorg-x11-utils
# PulseAudio build requirements.
%if %{with_pulseaudio}
BuildRequires: pulseaudio-libs-devel >= 0.9.11
BuildRequires: pulseaudio >= 0.9.11
%endif
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel >= 3.0.10
%endif

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
# no prelink on ARM yet
%ifnarch %{arm} %{aarch64}
BuildRequires: prelink
%endif
%ifarch %{jit_arches}
#systemtap build requirement.
BuildRequires: systemtap-sdt-devel
%endif

Requires: rhino
Requires: lcms2 >= 2.5
Requires: libjpeg = 6b
Requires: fontconfig
Requires: xorg-x11-fonts-Type1
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ant.
Requires: jpackage-utils >= 1.7.3-1jpp.2
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage base provides.
Provides: jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver} = %{epoch}:%{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{epoch}:%{version}-%{release}
Provides: java = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi = %{epoch}:%{version}
Provides: jndi-ldap = %{epoch}:%{version}
Provides: jndi-cos = %{epoch}:%{version}
Provides: jndi-rmi = %{epoch}:%{version}
Provides: jndi-dns = %{epoch}:%{version}
Provides: jaas = %{epoch}:%{version}
Provides: jsse = %{epoch}:%{version}
Provides: jce = %{epoch}:%{version}
Provides: jdbc-stdext = 4.1
Provides: java-sasl = %{epoch}:%{version}
Provides: java-fonts = %{epoch}:%{version}

# Obsolete older 1.6 packages as it cannot use the new bytecode
Obsoletes: java-1.6.0-openjdk
Obsoletes: java-1.6.0-openjdk-demo
Obsoletes: java-1.6.0-openjdk-devel
Obsoletes: java-1.6.0-openjdk-javadoc
Obsoletes: java-1.6.0-openjdk-src

%description
The OpenJDK runtime environment.

%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java-sdk-%{javaver} = %{epoch}:%{version}
Provides: java-sdk-%{origin} = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel = %{epoch}:%{version}
Provides: java-devel-%{origin} = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{javaver}


%description devel
The OpenJDK development tools.

%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description demo
The OpenJDK demos.

%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description src
The OpenJDK source bundle.

%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage javadoc provides.
Provides: java-javadoc = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
The OpenJDK API documentation.

%package accessibility
Summary: OpenJDK accessibility connector
Requires: java-atk-wrapper
Requires: %{name} = %{epoch}:%{version}-%{release}

%description accessibility
Enables accessibility support in OpenJDK by using java-at-wrapper. This allows compatible at-spi2 based accessibility programs to work for AWT and Swing-based programs.
Please note, the java-atk-wrapper is still in beta, and also OpenJDK itself is still in phase of tuning to be working with accessibility features.
Although working pretty fine, there are known issues with accessibility on, so do not rather install this package unless you really need.

%prep
%setup -q -c -n %{uniquesuffix} -T -a 0
cp %{SOURCE2} .

# OpenJDK patches
%patch100

# pulseaudio support
%if %{with_pulseaudio}
%patch300
%endif

# Add systemtap patches if enabled
%if %{with_systemtap}
%endif

# Remove libraries that are linked
sh %{SOURCE10}

# Copy jaxp, jaf and jaxws drops
mkdir drops/

# Extract the rewriter (to rewrite rhino classes)
tar xzf %{SOURCE5}

# Extract systemtap tapsets
%if %{with_systemtap}

tar xzf %{SOURCE6}

for file in tapset/*.in; do

    OUTPUT_FILE=`echo $file | sed -e s:%{javaver}\.stp\.in$:%{version}-%{release}.stp:g`
    sed -e s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/server/libjvm.so:g $file > $file.1
# FIXME this should really be %if %{has_client_jvm}
%ifarch %{ix86}
    sed -e s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/client/libjvm.so:g $file.1 > $OUTPUT_FILE
%else
    sed -e '/@ABS_CLIENT_LIBJVM_SO@/d' $file.1 > $OUTPUT_FILE
%endif
    sed -i -e s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir}:g $OUTPUT_FILE
    sed -i -e s:@INSTALL_ARCH_DIR@:%{archinstall}:g $OUTPUT_FILE

done

%endif

# Pulseaudio
%if %{with_pulseaudio}
tar xzf %{SOURCE9}
%endif


%patch3
%patch4

%if %{debug}
%patch5
%patch6
%endif

# Type fixes for s390
%patch101
%ifnarch %{arm}
%patch102
%patch110
%patch111
%patch112
%endif

%patch106
%patch200

%ifarch ppc ppc64
# PPC fixes
%patch104
%patch105
%endif

%ifarch %{jit_arches}
%patch402
%patch403
%endif

%patch404 -R

%build
# How many cpu's do we have?
%ifarch aarch64
# temporary until real hardware lands
export NUM_PROC=1
%else
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}
%endif

# Build IcedTea and OpenJDK.
%ifarch s390x sparc64 alpha %{power64} %{aarch64}
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

# Build the re-written rhino jar
mkdir -p rhino/{old,new}

# Compile the rewriter
(cd rewriter 
 javac com/redhat/rewriter/ClassRewriter.java
)

# Extract rhino.jar contents and rewrite
(cd rhino/old 
 jar xf /usr/share/java/rhino.jar
)

java -cp rewriter com.redhat.rewriter.ClassRewriter \
    $PWD/rhino/old \
    $PWD/rhino/new \
    org.mozilla \
    sun.org.mozilla

(cd rhino/old
 for file in `find -type f -not -name '*.class'` ; do
     new_file=../new/`echo $file | sed -e 's#org#sun/org#'`
     mkdir -pv `dirname $new_file`
     cp -v $file $new_file
     sed -ie 's#org\.mozilla#sun.org.mozilla#g' $new_file
 done
)

(cd rhino/new
   jar cfm ../rhino.jar META-INF/MANIFEST.MF sun
)

export JDK_TO_BUILD_WITH=/usr/lib/jvm/java-openjdk



pushd openjdk >& /dev/null

export ALT_DROPS_DIR=$PWD/../drops
export ALT_BOOTDIR="$JDK_TO_BUILD_WITH"

# Save old umask as jdk_generic_profile overwrites it
oldumask=`umask`

# Set generic profile
%ifnarch %{jit_arches}
export ZERO_BUILD=true
%endif
source jdk/make/jdk_generic_profile.sh

# Restore old umask
umask $oldumask

make \
  DISABLE_INTREE_EC=true \
  UNLIMITED_CRYPTO=true \
  ANT="/usr/bin/ant" \
  DISTRO_NAME="Fedora" \
  DISTRO_PACKAGE_VERSION="fedora-%{release}-%{_arch} u%{updatever}-b%{buildver}" \
  JDK_UPDATE_VERSION=`printf "%02d" %{updatever}` \
  JDK_BUILD_NUMBER=b`printf "%02d" %{buildver}` \
  MILESTONE="fcs" \
  HOTSPOT_BUILD_JOBS="$NUM_PROC" \
  STATIC_CXX="false" \
  RHINO_JAR="$PWD/../rhino/rhino.jar" \
  GENSRCDIR="$PWD/generated.build" \
  FT2_CFLAGS="-I/usr/include/freetype2 " \
  FT2_LIBS="-lfreetype " \
  DEBUG_CLASSFILES="true" \
  DEBUG_BINARIES="true" \
  STRIP_POLICY="no_strip" \
%ifnarch %{jit_arches}
  LIBFFI_CFLAGS="`pkg-config --cflags libffi` " \
  LIBFFI_LIBS="-lffi " \
  ZERO_BUILD="true" \
  ZERO_LIBARCH="%{archbuild}" \
  ZERO_ARCHDEF="%{archdef}" \
%ifarch ppc ppc64 s390 s390x
  ZERO_ENDIANNESS="big" \
%else
  ZERO_ENDIANNESS="little" \
  ZERO_ARCHFLAG="-D_LITTLE_ENDIAN" \
%endif
%endif
  %{debugbuild}

popd >& /dev/null

%ifarch %{jit_arches}
chmod 644 $(pwd)/%{buildoutputdir}/j2sdk-image/lib/sa-jdi.jar
%endif

export JAVA_HOME=$(pwd)/%{buildoutputdir}/j2sdk-image

# Build pulseaudio and install it to JDK build location
%if %{with_pulseaudio}
pushd pulseaudio
make JAVA_HOME=$JAVA_HOME -f Makefile.pulseaudio
cp -pPRf build/native/libpulse-java.so $JAVA_HOME/jre/lib/%{archinstall}/
cp -pPRf build/pulse-java.jar $JAVA_HOME/jre/lib/ext/
popd
%endif

# Copy tz.properties
echo "sun.zoneinfo.dir=/usr/share/javazi" >> $JAVA_HOME/jre/lib/tz.properties

#remove all fontconfig files. This change should be usptreamed soon
rm -f %{buildoutputdir}/j2re-image/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/j2re-image/lib/fontconfig*.bfc
rm -f %{buildoutputdir}/j2sdk-image/jre/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/j2sdk-image/jre/lib/fontconfig*.bfc
rm -f %{buildoutputdir}/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/lib/fontconfig*.bfc

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE11}
$JAVA_HOME/bin/java TestCryptoLevel


%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

# Install symlink to default soundfont
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/audio
pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/audio
ln -s %{_datadir}/soundfonts/default.sf2
popd

pushd %{buildoutputdir}/j2sdk-image

#install jsa directories so we can owe them
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

%ifarch %{jit_arches}
  # Install systemtap support files.
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset
  cp -a $RPM_BUILD_DIR/%{uniquesuffix}/tapset/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset/
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
  pushd $RPM_BUILD_ROOT%{jvmjardir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{uniquesuffix}/jce/vanilla

  # Install versioned symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{uniquesuffix}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

popd


# Install nss.cfg
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/


# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in %{SOURCE7} %{SOURCE77} ; do
    sed -i "s/#ARCH#/%{_arch}-%{release}/g" $e
    sed -i "s|/usr/bin|%{sdkbindir}/|g" $e
    desktop-file-install --vendor=%{uniquesuffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}.files
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files

# intentionally after the files generation, as it goes to separate package
# Create links which leads to separately installed java-atk-bridge and allow configuration
# links points to java-atk-wrapper - an dependence
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/%{archinstall}
    ln -s %{syslibdir}/java-atk-wrapper/libatk-wrapper.so.0 libatk-wrapper.so
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/ext
     ln -s %{syslibdir}/java-atk-wrapper/java-atk-wrapper.jar  java-atk-wrapper.jar
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/
    echo "#Config file to  enable java-atk-wrapper" > accessibility.properties
    echo "" >> accessibility.properties
    echo "assistive_technologies=org.GNOME.Accessibility.AtkWrapper" >> accessibility.properties
    echo "" >> accessibility.properties
  popd

#f19 only backward compatibility link
ln -s %{_jvmdir}/java-%{javaver}-%{origin} $RPM_BUILD_ROOT/%{_jvmdir}/java-%{javaver}-%{origin}.%{_arch}


# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%post
%ifarch %{jit_arches}
#see https://bugzilla.redhat.com/show_bug.cgi?id=513605
%{jrebindir}/java -Xshare:dump >/dev/null 2>/dev/null
%endif

# Note current status of alternatives
MAKE_THIS_DEFAULT=0
ID="%{_jvmdir}/\(\(jre\)\|\(java\)\)-%{javaver}-%{origin}.*bin/java"
COMMAND=java
alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
if [ $? -ne 0 ]; then
  alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
  if [ $? -eq 0 ]; then
    MAKE_THIS_DEFAULT=1
  fi
fi

# Remove old alternatives
for alt in $(alternatives --display $COMMAND | grep priority | awk '{print $1}'); do
  # Only grab what %{origin} installed
  echo $alt | grep -q "$ID"
  if [ $? -eq 0 ]; then
    alternatives --remove $COMMAND $alt >& /dev/null || :
   fi
done

ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jredir} \
  --slave %{_jvmjardir}/jre jre_exports %{jvmjardir} \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{uniquesuffix}.1$ext

%if %{graceful_links}
# Gracefully update to this one if needed
if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
  alternatives --set $COMMAND %{jrebindir}/java
%if %{graceful_links}
fi
%endif

for X in %{origin} %{javaver} ; do
  # Note current status of alternatives
  MAKE_THIS_DEFAULT=0
  ID="%{_jvmdir}/\(\(jre\)\|\(java\)\)-%{javaver}-%{origin}"
  COMMAND=jre_$X
  alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
  if [ $? -ne 0 ]; then
    alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
    if [ $? -eq 0 ]; then
      MAKE_THIS_DEFAULT=1
    fi
  fi

  # Remove old alternatives
  for alt in $(alternatives --display $COMMAND | grep priority | awk '{print $1}'); do
    # Only grab what %{origin} installed
    echo $alt | grep -q "$ID"
    if [ $? -eq 0 ]; then
      alternatives --remove $COMMAND $alt >& /dev/null || :
     fi
  done

  alternatives \
    --install %{_jvmdir}/jre-"$X" \
    jre_"$X" %{_jvmdir}/%{jredir} %{priority} \
    --slave %{_jvmjardir}/jre-"$X" \
    jre_"$X"_exports %{jvmjardir}
%if %{graceful_links}
  # Gracefully update to this one if needed
  if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
    alternatives --set $COMMAND %{_jvmdir}/%{jredir}
%if %{graceful_links}
  fi
%endif
done

update-alternatives --install %{_jvmdir}/jre-%{javaver}_%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_%{origin}_exports      %{jvmjardir}

update-desktop-database %{_datadir}/applications &> /dev/null || :

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0

%postun
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jredir}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jredir}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

exit 0

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post devel
# Note current status of alternatives
MAKE_THIS_DEFAULT=0
ID="%{_jvmdir}/java-%{javaver}-%{origin}.*bin/javac"
COMMAND=javac
alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
if [ $? -ne 0 ]; then
  alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
  if [ $? -eq 0 ]; then
    MAKE_THIS_DEFAULT=1
  fi
fi

# Remove old alternatives
for alt in $(alternatives --display $COMMAND | grep priority | awk '{print $1}'); do
  # Only grab what %{origin} installed
  echo $alt | grep -q "$ID"
  if [ $? -eq 0 ]; then
    alternatives --remove $COMMAND $alt >& /dev/null || :
   fi
done

ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdkdir} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt apt %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck extcheck %{sdkbindir}/extcheck \
  --slave %{_bindir}/idlj idlj %{sdkbindir}/idlj \
  --slave %{_bindir}/jar jar %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah javah %{sdkbindir}/javah \
  --slave %{_bindir}/javap javap %{sdkbindir}/javap \
  --slave %{_bindir}/jcmd jcmd %{sdkbindir}/jcmd \
  --slave %{_bindir}/jconsole jconsole %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb jdb %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat jhat %{sdkbindir}/jhat \
  --slave %{_bindir}/jinfo jinfo %{sdkbindir}/jinfo \
  --slave %{_bindir}/jmap jmap %{sdkbindir}/jmap \
  --slave %{_bindir}/jps jps %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir}/jsadebugd \
  --slave %{_bindir}/jstack jstack %{sdkbindir}/jstack \
  --slave %{_bindir}/jstat jstat %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd jstatd %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/policytool policytool %{sdkbindir}/policytool \
  --slave %{_bindir}/rmic rmic %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen schemagen %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver serialver %{sdkbindir}/serialver \
  --slave %{_bindir}/wsgen wsgen %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport wsimport %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc xjc %{sdkbindir}/xjc \
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \
  %{_mandir}/man1/appletviewer-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/apt.1$ext apt.1$ext \
  %{_mandir}/man1/apt-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{uniquesuffix}.1$ext

# Gracefully update to this one if needed
%if %{graceful_links}
if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
  alternatives --set $COMMAND %{sdkbindir}/javac
%if %{graceful_links}
fi
%endif

for X in %{origin} %{javaver} ; do
  # Note current status of alternatives
  MAKE_THIS_DEFAULT=0
  ID="%{_jvmdir}/java-%{javaver}-%{origin}"
  COMMAND=java_sdk_$X
  alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
  if [ $? -ne 0 ]; then
    alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
    if [ $? -eq 0 ]; then
      MAKE_THIS_DEFAULT=1
    fi
  fi

  # Remove old alternatives
  for alt in $(alternatives --display $COMMAND | grep priority | awk '{print $1}'); do
    # Only grab what %{origin} installed
    echo $alt | grep -q "$ID"
    if [ $? -eq 0 ]; then
      alternatives --remove $COMMAND $alt >& /dev/null || :
     fi
  done

  alternatives \
    --install %{_jvmdir}/java-"$X" \
    java_sdk_"$X" %{_jvmdir}/%{sdkdir} %{priority} \
    --slave %{_jvmjardir}/java-"$X" \
    java_sdk_"$X"_exports %{_jvmjardir}/%{sdkdir}

%if %{graceful_links}
  # Gracefully update to this one if needed
  if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
    alternatives --set $COMMAND %{_jvmdir}/%{sdkdir}
%if %{graceful_links}
  fi
%endif
done

update-alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}-%{origin}       java_sdk_%{javaver}_%{origin}_exports      %{_jvmjardir}/%{sdkdir}


exit 0

%postun devel
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir}
  alternatives --remove java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir}

exit 0

%post javadoc
MAKE_THIS_DEFAULT=0
ID="%{_javadocdir}/java-%{javaver}-%{origin}.*/api"
COMMAND=javadocdir
alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
if [ $? -ne 0 ]; then
  alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
  if [ $? -eq 0 ]; then
    MAKE_THIS_DEFAULT=1
  fi
fi

# Remove old alternatives
for alt in $(alternatives --display $COMMAND | grep priority | awk '{print $1}'); do
  # Only grab what %{origin} installed
  echo $alt | grep -q "$ID"
  if [ $? -eq 0 ]; then
    alternatives --remove $COMMAND $alt >& /dev/null || :
   fi
done

alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir}/api \
  %{priority}

%if %{graceful_links}
# Gracefully update to this one if needed
if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
  alternatives --set $COMMAND %{_javadocdir}/%{uniquejavadocdir}/api
%if %{graceful_links}
fi
%endif

exit 0

%postun javadoc
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir}/api

exit 0


%files -f %{name}.files
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/ASSEMBLY_EXCEPTION
%doc %{_jvmdir}/%{sdkdir}/LICENSE
%doc %{_jvmdir}/%{sdkdir}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/logging.properties
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}.png
%{_mandir}/man1/java-%{uniquesuffix}.1*
%{_mandir}/man1/keytool-%{uniquesuffix}.1*
%{_mandir}/man1/orbd-%{uniquesuffix}.1*
%{_mandir}/man1/pack200-%{uniquesuffix}.1*
%{_mandir}/man1/rmid-%{uniquesuffix}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix}.1*
%{_mandir}/man1/servertool-%{uniquesuffix}.1*
%{_mandir}/man1/tnameserv-%{uniquesuffix}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix}.1*
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/nss.cfg
%{_jvmdir}/%{jredir}/lib/audio/
%ifarch %{jit_arches}
%attr(664, root, root) %ghost %{_jvmdir}/%{jredir}/lib/%{archinstall}/server/classes.jsa
%attr(664, root, root) %ghost %{_jvmdir}/%{jredir}/lib/%{archinstall}/client/classes.jsa
%endif
%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/
%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/
%{_sysconfdir}/.java/
%{_sysconfdir}/.java/.systemPrefs
%{_jvmdir}/java-%{javaver}-%{origin}.%{_arch}


%files devel
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/ASSEMBLY_EXCEPTION
%doc %{_jvmdir}/%{sdkdir}/LICENSE
%doc %{_jvmdir}/%{sdkdir}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%ifarch %{jit_arches}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmjardir}/%{sdkdir}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{uniquesuffix}.1*
%{_mandir}/man1/apt-%{uniquesuffix}.1*
%{_mandir}/man1/extcheck-%{uniquesuffix}.1*
%{_mandir}/man1/idlj-%{uniquesuffix}.1*
%{_mandir}/man1/jar-%{uniquesuffix}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix}.1*
%{_mandir}/man1/javac-%{uniquesuffix}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix}.1*
%{_mandir}/man1/javah-%{uniquesuffix}.1*
%{_mandir}/man1/javap-%{uniquesuffix}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix}.1*
%{_mandir}/man1/jdb-%{uniquesuffix}.1*
%{_mandir}/man1/jhat-%{uniquesuffix}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix}.1*
%{_mandir}/man1/jmap-%{uniquesuffix}.1*
%{_mandir}/man1/jps-%{uniquesuffix}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix}.1*
%{_mandir}/man1/jsadebugd-%{uniquesuffix}.1*
%{_mandir}/man1/jstack-%{uniquesuffix}.1*
%{_mandir}/man1/jstat-%{uniquesuffix}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix}.1*
%{_mandir}/man1/native2ascii-%{uniquesuffix}.1*
%{_mandir}/man1/policytool-%{uniquesuffix}.1*
%{_mandir}/man1/rmic-%{uniquesuffix}.1*
%{_mandir}/man1/schemagen-%{uniquesuffix}.1*
%{_mandir}/man1/serialver-%{uniquesuffix}.1*
%{_mandir}/man1/wsgen-%{uniquesuffix}.1*
%{_mandir}/man1/wsimport-%{uniquesuffix}.1*
%{_mandir}/man1/xjc-%{uniquesuffix}.1*
%ifarch %{jit_arches}
%{tapsetroot}
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/LICENSE

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir}
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE

%files accessibility
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libatk-wrapper.so
%{_jvmdir}/%{jredir}/lib/ext/java-atk-wrapper.jar
%{_jvmdir}/%{jredir}/lib/accessibility.properties

%changelog
* Tue Sep 24 2013 Omair Majid <omajid@rehdat.com> - 1.7.0.40-2.4.2.5.f19
- Fix paths in tapsets for non x86_64 archs
- Allow tapsets to use client jvm on i386

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.7.0.40-2.4.2.4.f19
- don't apply more patches on ARM

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.7.0.40-2.4.2.3.f19
- don't apply the size_t patch on ARM

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.7.0.40-2.4.2.2.f19
- fix build on zero arches (Andrew Hughes <gnu.andrew@redhat.com)

* Wed Sep 11 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.1.f19
- buildver replaced by updatever
- buildver reset to 60
- updatever set to 40
- added   JDK_BUILD_NUMBER=b`printf "%02d" buildver to make parameters
- buildversion included in id
- desktop icons extracted to text files

* Fri Sep 06 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.4.2.0.f19
- updated to icedtea7-forest 2.4.2
- removed upstreamed patch404  aarch64.patch
- adapted patch104 java-1.7.0-openjdk-ppc-zero-jdk.patch
- adapted patch105 java-1.7.0-openjdk-ppc-zero-hotspot.patch
- added patch404 RH661505-toBeReverted.patch, to be *reverted* during prep
- buildver bumbed to 60

* Mon Sep 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.4.1.4.f19
- buildver bumbed to 31
- switched back to system lcms2
 - removed patch 500 java-1.7.0-openjdk-disable-system-lcms
 - added requires for lcms2 > 2.5
- removed unnecessary patch 112 java-1.7.0-openjdk-doNotUseDisabledEcc.patch
- added and used after build source 11, TestCryptoLevel.java

* Mon Sep 02 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.4.1.1.f19
- updated to icedtea 2.4
 - added java-1.7.0-openjdk-doNotUseDisabledEcc.patch
 - deleted usptreamed 657854-openjdk7.patch
 - deleted usptreamed callerclass-01.patch
 - deleted usptreamed callerclass-02.patch
 - deleted usptreamed callerclass-03.patch
 - deleted usptreamed callerclass-04.patch
 - deleted usptreamed systemtap.patch
 - added new file fsg.sh - to celan up sources
 - adapted  aarch64.patch
 - adapted  gstackbounds.patch
 - adapted  java-1.7.0-openjdk-disable-system-lcms.patch
 - adapted  java-1.7.0-openjdk-java-access-bridge-security.patch
 - adapted  java-1.7.0-openjdk-ppc-zero-hotspot.patch
 - adapted  java-1.7.0-openjdk-size_t.patch
 - adapted  java-1.7.0-openjdk.spec
 - adapted  rhino.patch
- temporarily disabled arm32 support (will need duplicated source tarball based
  on 3.x or deeper fix for 2.4.x)

* Tue Aug 20 2013 Omair Majid <omajid@redhat.com> -1.7.0.25-2.3.12.4c20
- Backport getCallerClass-related patches from upstream that are not in a release yet

* Sat Jul 27 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.12.3.f20
- setting of alternatives moved into conditional block controlled by graceful_links
- added graceful_links, set to disabled (0)

* Fri Jul 26 2013 Orion Poplawski <orion@cora.nwra.com> - 1.7.0.25-2.3.12.2.fc19
- Fix broken jre_exports alternatives links (bug #979128)

* Fri Jul 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.12.1.f19
- refreshed icedtea7-forest 2.3.12

* Thu Jul 25 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.11.0.f19
- finally merged arm and main source tarballs
- updated to icedtea 2.3.11
 - http://blog.fuseyism.com/index.php/2013/07/25/icedtea-2-3-11-released/
- added removal of new jre-1.7.0-openjdk and java-1.7.0-openjdk alternatives
- removed patch 400, rhino for 2.1 and other 2.1 conditional stuff
- removed patch 103 arm-fixes.patch
- added ZERO_ARCHFLAG="-D_LITTLE_ENDIAN"  for zero (arm) builds

* Wed Jul 24 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.11.f19
- added support for aarch64
 - aarch64 variable to be used in conditions where necessary
 - patch404  aarch64.patch (author: msalter) to add aarch64 support to makefiles
 (needs more tweeking!)
- added new alternatives jre-1.7.0-openjd and java-1.7.0-openjdk to keep
 backward comaptibility after uniquesuffix and add/remove alternatives approach
- removed arm_arches variable in favour of standart arm one
- added java-1.7.0-openjdk.arch symlink for backward-backward compatibility.
 - _jvmdir/java-javaver-origin._arch

* Mon Jul 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.10.f19
- removed _jvmdir/sdkdir from devel files

* Fri Jul 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.9.f19
- ID values are now in quotes

* Fri Jul 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.8.f19
- jrelnk is now just lnk, everything is pointing through jredir
- all alternatives are celaned before new one is added
- alternatives are removed after uninstall

* Thu Jul 18 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.8.f19
- moved to full-version directory
- moved to add/remove alternatives process
- sdklnk removed, and substitued by  sdkdir

* Wed Jul 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.7.f19
- moved to xz compression of sources
- updated 2.1 tarball

* Thu Jun 27 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.4.f19
- Sync with upstream IcedTea7-forest 2.3.10 tag
- Fixes regressions as introduced with previous 1.7.0.25 updates
  - rhbz#978005, rhbz#977979, rhbz#976693, IcedTeaBZ#1487.

* Wed Jun 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.3.fc19
- update of IcedTea7-forest 2.3.10 tarball

* Thu Jun 13 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.2.fc19
- added patch1000 MBeanFix.patch to fix regressions caused by security patches

* Thu Jun 13 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.1.fc19
- arm tarball updated to 2.1.9
- build bumped to 25

* Wed Jun 12 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.10.0.fc19
- All full-paths now have arch
- temporarly swithced to intree lcms as it have security fixes (patch 500)
 - added  GENSRCDIR="$PWD/generated.build" to be able to
 - removed (build)requires  lcms2(-devel)
- Updated to latest IcedTea7-forest 2.3.10

* Wed Jun 05 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.12.fc19
- Added client/server directories so they can be owned
- More usage of uniquesuffix
- Renamed patch 107 to 200
- Added fix for RH857717, owned /etc/.java/ and /etc/.java/.systemPrefs

* Wed May 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.11.fc19
- added variable arm_arches as restriction to some cases of not jit_arches
- size_t patch adapted to 2.3 which is now default on all except arm arches

* Fri May 17 2013 Omair Majid <omajid@redhat.com> - 1.7.0.19-2.3.9.10.fc20
- Replace %{name} with %{uniquesuffix} where it's used as a unique suffix.

* Tue May 14 2013 Jiri Vanek <jvanek@redhat.com> 1.7.0.19-2.3.9.9.fc19
- patch402 gstackbounds.patch applied only to jit arches
- patch403 PStack-808293.patch likewise

* Mon May 13 2013 Jiri Vanek <jvanek@redhat.com>
- enhancements to icons
 - now points to openjdk directly instead though alternatives
 - contains full version id

* Fri May 10 2013 Adam Williamson <awilliam@redhat.com>
- update scriptlets to follow current guidelines for updating icon cache

* Tue May 07 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.7.fc19
- added patch 401 657854-openjdk7.patch (see 947731)
- fixed icons (see https://bugzilla.redhat.com/show_bug.cgi?id=820619)
- added patch 402 gstackbounds.patch - see (RH902004)
- added patch 403 PStack-808293.patch - to work more about jstack

* Mon Apr 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.6.fc19
- cosmetic changes to  accessibility subpackage
 - removed all provides
 - changed description a bit
- removed incorrect noarch tag from accessibility subpackage

* Mon Apr 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.5.fc19
- created accessibility subpackage
 - all intentionally broken java-ark-wrapper symlinks placed here

* Mon Apr 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.4.fc19
- removed bootstrap

* Fri Apr 19 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.19-2.3.9.3.fc19
- Updated 2.1.8 tarball
- Forcibly remove bfc files

* Thu Apr 18 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.19-2.3.9.2.fc19
- Updated secondary arches to 2.1.8
- Removed upstreamed Zero allocation patch

* Tue Apr 16 2013 Jiri Vanek <jvanek@redhat.com - 1.7.0.19-2.3.9.1.fc19
- updated to IcedTea  2.3.9 with latest security patches
  - updated to updated IcedTea  2.3.9 with fix to one of security fixes
  -  fixed font glyph offset
- added client to ghosted classes.jsa
- buildver sync to b19
- rewritten java-1.7.0-openjdk-java-access-bridge-security.patch


* Wed Apr 10 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.6.fc19
- fixed priority (one zero deleted)
- unapplied patch2

* Thu Apr 04 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.6.fc19
- added patch107 abrt_friendly_hs_log_jdk7.patch
- removed patch2   java-1.7.0-openjdk-java-access-bridge-idlj.patch

* Wed Apr 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.5.fc19
- removed redundant rm of classes.jsa, ghost is handling it correctly
- removed access-gnome-bridge as deprecated technology.
 - replaced by linking to optional, install-able,  package java-atk-wrapper
 - all patches kept as valid in same way as for gnome bridge
 - question is java-1.7.0-openjdk-java-access-bridge-idlj if still valid
- commented out mysterious patch2   java-1.7.0-openjdk-java-access-bridge-idlj.patch
 - candidate for deletation

* Fri Mar 29 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.4.fc19
- Updated to java-access-bridge-1.26.2.tar.bz2

* Tue Mar 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.3.fc19
- added manual deletion of classes.jsa
- ghost classes.jsa restricted to jitarches and to full path
- zlib in BuildReq restricted for  1.2.3-7 or higher
 - see https://bugzilla.redhat.com/show_bug.cgi?id=904231

* Tue Mar 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.2.fc19
- Removed a -icedtea tag from the version
  - package have less and less connections to icedtea7
- Added link to nss as noreplace bug to previous changelog item

* Mon Mar 25 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.1.fc19
- Bumped release
- Added and applied patch500 java-1.7.0-openjdk-fixZeroAllocFailure.patch
  - to fix not-jit arches build
  - is already in upstreamed icedtea 2.1
- Added gcc-c++ build dependence. Sometimes caused troubles during rpm -bb
- Added (Build)Requires for fontconfig and xorg-x11-fonts-Type1
  - see https://bugzilla.redhat.com/show_bug.cgi?id=721033 for details
- Removed all fonconfig files. Fonts are now handled differently in JDK 
  and those files are redundant. This is going to be usptreamed.
  - see https://bugzilla.redhat.com/show_bug.cgi?id=902227 for details
- logging.properties marked as config(noreplace)
  - see https://bugzilla.redhat.com/show_bug.cgi?id=679180 for details
- classes.jsa marked as ghost 
  - see https://bugzilla.redhat.com/show_bug.cgi?id=918172 for details
- nss.cfg was marked as config(noreplace) 
  - see https://bugzilla.redhat.com/show_bug.cgi?id=913821 for details

* Mon Mar 04 2013 Omair Majid <omajid@redhat.com> - 1.7.0.9-2.3.8.fc19
- Updated to icedtea7 2.3.8 (forest)
- Removed upstreamed patches.

* Sat Feb 16 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.7.fc19
- Updated to 2.3.7 icedtea7 tarball
- Updated the 2.1.6 icedtea7 tarballfor arm
- Removed testing
 - mauve was outdated and
 - jtreg was icedtea relict
- Added java -Xshare:dump to post (see 513605) fo jitarchs

* Thu Feb 14 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.6.fc19
- Updated to 2.3.6
- Updated the 2.1.5 tarball
- Removed upstreamed patches (Patch1000+)

* Thu Feb 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.0.9-2.3.5.5.fc19
- rebuild for ARM fix

* Mon Feb 11 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.4.fc19
- Updated secondary arch tarball to 2.1.5
- Made Patch100* jit-arch specific-only (not needed for 2.1.5)

* Thu Feb 07 2013 Omair Majid <omajid@redhat.com> - 1.7.0.9-2.3.5.3.fc19
- Sync logging fixes with upstream (icedtea7-forest and jdk7u)

* Thu Feb 07 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.1.fc19
- Added patch for 8005615 to fix regression caused by fix for 6664509

* Wed Feb 06 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.fc19.1
- Backed out 6664509 and 7201064.patch which cause regressions

* Sun Feb 03 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.fc19
- Bumped to 2.3.5
- Removed unnecessary GENSRC flag

* Sun Feb 03 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.4.2.fc19
- Bumped to 2.3.5pre (2.3.4 + Feb. 2013 CPU)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1:1.7.0.9-2.3.4.1.1
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.4.1.fc19
- Added idlj slave to javac
- Added jcmd slave to javac
- Release incremented

* Mon Jan 14 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.4.fc19
- Updated to 2.3.4

* Thu Dec 06 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.2.fc19.2
- introduced tmp-patches source tarball 
- added kerberos fix (see rhbz#871771)
- added OpenOffice crusher fix (see oracle's 8004344)

* Wed Oct 17 2012 Dan Horák <dan[at]danny.cz> - 1.7.0.9-2.3.3.fc19.1
- change the permission of sa-jdi.jar only on jit_arches

* Tue Oct 16 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.3.fc19
- Updated to IcedTea7-forest 2.3.3 primary arches
- Updated to IcedTea7-forest 2.1.3 for secondary arches
- Change permission of sa-jdi.jar to 644 (upstream for future)
- Resolves rhbz#s 856124, 865346, 865348, 865350, 865352, 865354, 865357,
  865359, 865363, 865365, 865370, 865428, 865471, 865434, 865511, 865514,
  865519, 865531, 865541, 865568

* Fri Sep 7 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.1.fc19.3
- Not-jit-archs source tarball updated to openjdk-icedtea-2.1.2.tar.gz

* Thu Aug 30 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.1.fc19.2
- Updated to IcedTea-Forest 2.3.1
- Resolves rhbz#RH852051, CVE-2012-4681: Reintroduce PackageAccessible checks 
  removed in 6788531.
- Commented out Patch500, java-1.7.0-openjdk-removing_jvisualvm_man.patch as
  as already included in this Iced-Tea.
- Will be nice to verify after next upstream sync if it is still upstreamed

* Tue Aug 28 2012 Orcan Ogetbil <oget.fedora@gmail.com> - 1.7.0.6-2.3.fc19.1
- Add symlink to Fedora's default soundfont rhbz#541466

* Mon Aug 27 2012 Jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.fc19.1
- Updated to latest IcedTea7-forest-2.3
- Current build is u6
- ALT_STRIP_POLICY replaced by STRIP_POLICY
- Patch103 java-1.7.0-opendk-arm-fixes.patch split to itself and new 
  Patch106 java-1.7.0-opendk-freetype-check-fix.patch by meaning. Both applied.
- Added Patch500, java-1.7.0-openjdk-removing_jvisualvm_man.patch to remove 
  jvisualvm manpages from processing

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.0.5-2.2.1.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.5-2.2.1.fc18.9
- Added support to build older (2.1.1/u3/hs22) version on non-jit (secondary)
  arches

* Wed Jun 13 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.3-2.2.1fc18.8
- Fixed broken provides sections
- Changed java-devel requirement to be self's devel (java-1.7.0-openjdk-devel)

* Mon Jun 11 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.3-2.2.1fc18.7
- Used newly prepared tarball with security fixes
- Bump to icedtea7-forest-2.2.1
- _mandir/man1/jcmd-name.1 added to alternatives
- Updated rhino.patch
- Modified partially upstreamed patch302 - systemtap.patch
- Temporarly disabled patch102 - java-1.7.0-openjdk-size_t.patch
- Removed already upstreamed patches 104,107,108,301
  - java-1.7.0-openjdk-arm-ftbfs.patch
  - java-1.7.0-openjdk-system-zlib.patch
  - java-1.7.0-openjdk-remove-mimpure-opt.patch
  - systemtap-alloc-size-workaround.patch
- patch 105 (java-1.7.0-openjdk-ppc-zero-jdk.patch) have become 104
- patch 106 (java-1.7.0-openjdk-ppc-zero-hotspot.patch) have become 105
- Added build requires zip, which was untill now  dependence  of dependence
- Access gnome brridge jar forced to be 644

* Fri May 25 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.7
- Miscellaneous fixes brought in from RHEL branch
- Resolves: rhbz#825255: Added ALT_STRIP_POLICY so that debug info is not stripped
- Moved Patch #7 (usage of system zlib) to #107

* Tue May 01 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.6
- Removed VisualVM requirements
- Obsoleted java-1.6.0-openjdk*
- Added BR for zip

* Mon Mar 26 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.5
- Added SystemTap fixes by Mark Wielaard

* Sat Mar 24 2012 Dan HorÃ¡k <dan[at]danny.cz>> - 1.7.0.3-2.1.fc17.4
- update paths in the ppc patches, add missing snippet

* Wed Mar 21 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.3
- Reverted fix for rhbz#740762
- Fixed PPC/PPC64 build (rh804136) -- added patches from Chris Phillips
- Moved OpenJDK specific patches to 1XX series

* Mon Mar 12 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.2
- Resolved rhbz#740762: java.library.path is missing some paths
- Unified spec file for x86, x86_64, ARM and s390
  - Integrated changes from Dan HorÃ¡k <dhorak@redhat.com> for Zero/s390
  - Integrated changes from Chris Phillips <chphilli@redhat.com> for Zero/ARM

* Fri Feb 24 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.1
- Added flag so that debuginfo is built into classfiles (rhbz# 796400)
- Updated rhino.patch to build scripting support (rhbz# 796398)

* Tue Feb 14 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1
- Updated to OpenJDK7u3/IcedTea7 2.1
- Security fixes:
  - S7112642, CVE-2012-0497: Incorrect checking for graphics rendering object
  - S7082299, CVE-2011-3571: AtomicReferenceArray insufficient array type check
  - S7110687, CVE-2012-0503: Unrestricted use of TimeZone.setDefault
  - S7110700, CVE-2012-0505: Incomplete info in the deserialization exception
  - S7110683, CVE-2012-0502: KeyboardFocusManager focus stealing
  - S7088367, CVE-2011-3563: JavaSound incorrect bounds check
  - S7126960, CVE-2011-5035: Add property to limit number of request headers to the HTTP Server
  - S7118283, CVE-2012-0501: Off-by-one bug in ZIP reading code
  - S7110704, CVE-2012-0506: CORBA fix
- Add patch to fix compilation with GCC 4.7

* Tue Nov 15 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.1-2.0.3
- Added patch to fix bug in jdk_generic_profile.sh
- Compile with generic profile to use system libraries
- Made remove-intree-libraries.sh more robust
- Added lcms requirement
- Added patch to fix glibc name clash
- Updated java version to include -icedtea

* Sun Nov 06 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.1-2.0.2
- Added missing changelog entry

* Sun Nov 06 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.1-2.0.1
- Updated to IcedTea 2.0 tag in the IcedTea OpenJDK7 forest
- Removed obsoleted patches
- Added system timezone support
- Revamp version/release naming scheme to make it proper
- Security fixes
  - S7000600, CVE-2011-3547: InputStream skip() information leak
  - S7019773, CVE-2011-3548: mutable static AWTKeyStroke.ctor
  - S7023640, CVE-2011-3551: Java2D TransformHelper integer overflow
  - S7032417, CVE-2011-3552: excessive default UDP socket limit under SecurityManager
  - S7046823, CVE-2011-3544: missing SecurityManager checks in scripting engine
  - S7055902, CVE-2011-3521: IIOP deserialization code execution
  - S7057857, CVE-2011-3554: insufficient pack200 JAR files uncompress error checks
  - S7064341, CVE-2011-3389: HTTPS: block-wise chosen-plaintext attack against SSL/TLS (BEAST)
  - S7070134, CVE-2011-3558: HotSpot crashes with sigsegv from PorterStemmer
  - S7077466, CVE-2011-3556: RMI DGC server remote code execution
  - S7083012, CVE-2011-3557: RMI registry privileged code execution
  - S7096936, CVE-2011-3560: missing checkSetFactory calls in HttpsURLConnection

* Mon Aug 29 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110823.1
- Provide a "7" version of items to enfore F-16 policy of no Java 7 builds
- Resolves: rhbz#728706,  patch from Ville Skyttä <ville.skytta at iki dot fi>

* Fri Aug 05 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110803
- Use a newer snapshot and forest on classpath.org rather than on openjdk.net
- Added in-tree-removal script to remove libraries that we manually link
- Updated snapshots
- Added DISTRO_NAME and FreeType header/lib locations
- Removed application of patch100 and patch 113 (now in forest)

* Wed Aug 03 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110729
- Initial build from java-1.6.0-openjdk RPM
