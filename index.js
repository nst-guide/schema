const Ajv = require('ajv')
const ajv = new Ajv()

const schemaNames = ['town']

function loadSchemas() {
  let loaded_ajv = ajv
  for (const schemaName of schemaNames) {
    const schema = require(`./schemas/${schemaName}.json`)
    loaded_ajv = loaded_ajv.addSchema(schema, schemaName)
  }
  return loaded_ajv
}

function compile(schemaName) {
  return loadSchemas().getSchema(schemaName.toLowerCase())
}

function validate(instance, schemaName) {
  const validate = compile(schemaName)
  const valid = validate(instance)
  if (!valid) throw validate.errors
}

exports.compile = compile
exports.validate = validate
