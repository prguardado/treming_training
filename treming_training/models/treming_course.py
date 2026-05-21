from odoo import models, fields, api #, ValidationError
from odoo.exceptions import ValidationError

class TremingCourse(models.Model):
    _name = 'treming.course'
    _description = 'Training Course'
    
    name = fields.Char(required=True)
    code = fields.Char(required=True, unique=True)
    description = fields.Text()
    # Cambié de apuntador a res.users para el campo responsible_id, anterior estaba res.partner
    responsible_id = fields.Many2one('res.users', string='Responsible')
    partner_id = fields.Many2one('res.partner', string='Partner')
    start_date = fields.Date(required = True)
    end_date = fields.Date()
    duration_hours = fields.Float(required=True)    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft')
    
    active = fields.Boolean(default=True)
    
    # campo notes (HMTL)
    notes = fields.Html(string='Notes')
    
    # Añadida una restricción SQL para el campo code para que sea único ---------------------------
    _check_code = models.Constraint(
        'UNIQUE(code)',
        'El código del curso debe ser único.'
    )

    def action_confirm(self):
        for c in self:
            if c.state == 'draft':
                c.state = 'confirmed'
          
    def action_done(self):
        for c in self:
            if c.state == 'confirmed':
                c.state = 'done'
    
    def action_cancel(self):
        for c in self:
            if c.state in ['draft', 'confirmed']:
                c.state = 'cancelled'
                  
    def action_reset_to_draft(self):
        for c in self:
            if c.state in ['confirmed', 'done', 'cancelled']:
                c.state = 'draft'

    @api.constrains('duration_hours')
    def _check_duration(self):
        for c in self:
            if c.duration_hours <= 0:
                raise ValidationError("Duración debe ser mayor a 0 horas")
            
    @api.constrains('end_date', 'start_date')
    def _check_dates(self):
        for c in self:
            if c.end_date and c.start_date and c.end_date < c.start_date:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio")
            
            