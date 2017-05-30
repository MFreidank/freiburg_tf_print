from subprocess import check_call, CalledProcessError


def check_package_installed(package_name):
        import apt
        # try finding it using 'apt-cache(1)' and 'which(1)'
        cache = apt.Cache()
        try:
            cache.open()
            if not cache[package_name].is_installed:
                # check if 'which(1)' can find it..
                try:
                    check_call(["which", package_name])
                except CalledProcessError:
                    raise ValueError("Tried finding package '{}' using 'apt(1)' and 'which(1)' but failed. Is it installed? try running: 'sudo apt-get install {}' or set an appropriate symlink.".format(package_name))
                finally:
                    cache.close()
        finally:
            cache.close()
