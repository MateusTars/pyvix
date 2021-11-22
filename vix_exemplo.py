import pyvix

client = pyvix.VIXClient()
episodes = client.get_episodes_info('doomsday_pt')