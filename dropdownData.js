// Department codes extracted from index.html
const departments = [
  "AAAS", "AMEL", "AMES", "ANTH", "ARAB", "ARTH", "ASTR", 
  "BIOL", "CHEM", "CHIN", "CLST", "COCO", "COGS", "COLT", "COSC",
  "EARS", "ECON", "EDUC", "ENGL", "ENGS", "ENVS", "FILM", "FREN", "FRIT",
  "GEOG", "GERM", "GOVT", "GRK", "HEBR", "HIST", "HUM", "INTS", "ITAL",
  "JAPN", "JWST", "LACS", "LAT", "LATS", "LING", "M&SS", "MATH", "MUS",
  "NAS", "PBPL", "PHIL", "PHYS", "PORT", "PSYC", "REL", "RUSS", "SART",
  "SOCY", "SPAN", "SPEE", "SSOC", "THEA", "TUCK", "WGST", "WPS", "WRIT"
];

// Generate course numbers 1-200
const courseNumbers = Array.from({length: 200}, (_, i) => i + 1);

// Export both arrays for use in other files
export { departments, courseNumbers };
