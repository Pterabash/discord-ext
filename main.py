import blurpo

if __name__ == '__main__':
    blurpo.load_env()
    blurpo.load_local('blurpo.ext.code')
    blurpo.load_local('blurpo.ext.whitelist')
    blurpo.run()
