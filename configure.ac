#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT(FULL-PACKAGE-NAME, VERSION, BUG-REPORT-ADDRESS)

# Checks for programs.
AC_PROG_INSTALL
AC_PROG_MAKE_SET

AC_CONFIG_SRCDIR([Makefile.am])
AM_CONFIG_HEADER([config.h])
AC_CONFIG_AUX_DIR(.)

AM_INIT_AUTOMAKE([dist-bzip2])

AM_MAINTAINER_MODE

# Checks for programs.
AC_DISABLE_STATIC
AC_PROG_LIBTOOL
AC_PROG_CC

AC_ARG_WITH(arch,         AS_HELP_STRING([--with-arch=ARCH], [Architecture (default: arm)]),
                                [ ARCH="$withval" ],
                                [ ARCH="arm" ])
AC_ARG_WITH(conf-prefix,      AS_HELP_STRING([--with-conf-prefix=CONF_PREFIX], [Architecture (default: /opt/etc)]),
                                [ CONF_PREFIX="$withval" ],
                                [ CONF_PREFIX="/opt/etc" ])

AC_SUBST(ARCH)
AC_SUBST(CONF_PREFIX)

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
