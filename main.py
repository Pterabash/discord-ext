import nexity

if __name__ == '__main__':
    nexity.load_env()
    nexity.load_local('nexity.ext.code')
    nexity.load_local('nexity.ext.whitelist')
    nexity.run()
