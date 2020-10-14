import json


def get_prefix(guild):
    with open('./src/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(guild.id)]
   

def change_prefix(ctx, new_prefix: str):
    with open('./src/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    logging.debug(f'{ctx.author} (user id {ctx.author.id}) changed the prefix of {ctx.guild} (guild id {ctx.guild.id}) from '{prefixes[str(guild.id)]}')
    prefixes[str(ctx.guild.id)] = new_prefix
    with open('./src/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
