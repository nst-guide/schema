const Ajv = require('ajv');

const schemaNames = ['town', 'common'];

function loadSchemas() {
  let ajv = new Ajv();
  for (const schemaName of schemaNames) {
    const schema = require(`./schemas/${schemaName}.json`);
    ajv = ajv.addSchema(schema, schemaName);
  }
  return ajv;
}

function compile(schemaName) {
  return loadSchemas().getSchema(schemaName.toLowerCase());
}

function validate(instance, schemaName) {
  const validate = compile(schemaName);
  const valid = validate(instance);
  if (!valid) throw validate.errors;
  return valid;
}

exports.compile = compile;
exports.validate = validate;
