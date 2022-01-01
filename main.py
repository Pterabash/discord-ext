import blurpo


if __name__ == '__main__':
    blurpo.load_url('thisgary/blurple-o/main/blurpo/ext/code.py')
    blurpo.load_ext('blurpo.ext.whitelist')
    blurpo.load_env()
    blurpo.run()
