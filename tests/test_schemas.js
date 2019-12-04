const nstschema = require('../index.js');

const { readdirSync, readFileSync } = require('fs');
const glob = require('glob');

const getDirectories = source =>
  readdirSync(source, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .filter(dirent => dirent.name !== '__pycache__')
    .map(dirent => dirent.name);

const testFolders = getDirectories(__dirname);

describe('Test each tests folder', () => {
  for (const folder of testFolders) {
    const testFiles = glob.sync(__dirname + '/' + folder + '/*.json');
    for (const file of testFiles) {
      it('Should validate correctly', () => {
        const instance = JSON.parse(readFileSync(file));
        const valid = nstschema.validate(instance, folder);
        expect(valid).toBe(true);
      });
    }
  }
});
