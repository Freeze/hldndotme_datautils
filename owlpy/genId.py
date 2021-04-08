from datetime import datetime


def generateId(sighting):
    id = ""
    sighting_dt_obj = datetime.strptime(sighting['obsDt'], '%Y-%m-%d %H:%M')
    sighting_epoch = sighting_dt_obj.timestamp()
    sighting_loc_id = sighting['locId']
    sighting_species_code = sighting['speciesCode']
    id = "%s_%s_%s" %(sighting_species_code, sighting_epoch, sighting_loc_id)
    return id
