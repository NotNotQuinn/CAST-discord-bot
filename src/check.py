admins = {
        345701772016222209: 'Quinn'
    }

def is_admin(ctx):
    return ctx.author.id in admins
