export const getFullName = function (name) {
    let fullName = [];
    if(name['titles']) {
      fullName = fullName.concat(name['titles']+ ' ')
    }
    if(name['surname']){
      fullName = fullName.concat(name['surname']+ ', ')
    }
    if(name['forename']){
      fullName = fullName.concat(name['forename']+ ' ')
    }
    if(name['affix']){
      fullName = fullName.concat(name['affix'])
    }
    return fullName;
}

export const parties = {
    afd: "AfD",
    cdu: "CDU",
    linke: "DIE LINKE",
    fdp: "FDP",
    gruene: "GRÜNE",
    spd: "SPD"
};
