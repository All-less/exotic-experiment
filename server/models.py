import motor.motor_tornado

client = motor.motor_tornado.MotorClient()
db = client.exotic_database

User = db.user
Rpi = db.rpi
Admin = db.admin
