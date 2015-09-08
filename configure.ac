#  Copyright (c) 2011 Samsung Electronics Co., Ltd All Rights Reserved 
# 
#  Permission to use, copy, modify, distribute, and sell this software and its
#  documentation for any purpose is hereby granted without fee, provided that
#  the above copyright notice appear in all copies and that both that
#  copyright notice and this permission notice appear in supporting
#  documentation, and that the name of Red Hat not be used in
#  advertising or publicity pertaining to distribution of the software without
#  specific, written prior permission.  Red Hat makes no
#  representations about the suitability of this software for any purpose.  It
#  is provided "as is" without express or implied warranty.
# 
#  RED HAT DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
#  INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
#  EVENT SHALL RED HAT BE LIABLE FOR ANY SPECIAL, INDIRECT OR
#  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
#  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
#  TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
#  PERFORMANCE OF THIS SOFTWARE.
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
