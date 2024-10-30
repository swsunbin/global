#
# **************************************************************
# *                                                            *
# * Author: sunbin (2024)                                      *
# * URL: https://ftp.gnu.org/pub/gnu/global/				   *
# *                                                            *
# * Copyright notice:                                          *
# * Free use of this C++ Makefile template is permitted under  *
# * the guidelines and in accordance with the the MIT License  *
# * http://www.opensource.org/licenses/MIT                     *
# *                                                            *
# **************************************************************
#

TOPDIR := $(shell /bin/pwd)
core_src_dir = $(TOPDIR)
build_dir = $(TOPDIR)/build
global_src_dir = $(core_src_dir)/global-6.5.6
global_dest_dir = $(build_dir)/SOURCES/global-6.5.6
config_src_dir = $(TOPDIR)/config
global = global-6.5.6
all:  .build_global
  
.build_global:
	@(if [ -d $(build_dir) ]; then rm -rf $(build_dir); fi)
	@(mkdir -p $(build_dir)/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS})
	@(if [ -d $(global_dest_dir) ]; then mkdir -p $(global_dest_dir); fi)

	@echo "---------- copy global files ----------"
	@cp -a $(global_src_dir) $(global_dest_dir)
	@cp -a $(config_src_dir)/*  $(build_dir)/SOURCES
	@(cd $(build_dir)/SOURCES; \
		tar zcvf $(global).tar.gz $(global); \
		rm -rf $(global))

	@echo "---------- copy spec ----------"
	@(cp -af $(core_src_dir)/global.spec $(build_dir)/SPECS/)

	@echo "---------- build global ----------"
	@(rpmbuild -ba --define="_topdir $(build_dir)" $(build_dir)/SPECS/global.spec)

install:
	@(cd $(build_dir)/RPMS/x86_64; rpm -vih *.x86_64.rpm --force)
clean:
	-rm -rf $(build_dir)
