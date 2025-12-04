const mongoose = require('mongoose');

const EmailHistorySchema = new mongoose.Schema({
  subject: { type: String, required: true },
  recipients: { type: [String], default: [] },
  recipientsCount: { type: Number, default: 0 },
  status: { type: String, enum: ['sent','failed','pending'], default: 'pending' },
  info: { type: mongoose.Schema.Types.Mixed },
  sentBy: { type: String },
  sentAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('EmailHistory', EmailHistorySchema, 'email_history');
