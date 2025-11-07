# -*- coding: utf-8 -*-
from odoo import fields, models

class GithubWebhookLog(models.Model):
    _name = "github.webhook.log"
    _description = "GitHub Webhook Log"
    _order = "create_date desc"

    name = fields.Char("Título", index=True)
    repository = fields.Char("Repositorio")
    repo_owner = fields.Char("Owner")
    pr_number = fields.Integer("PR #")
    html_url = fields.Char("URL del PR")
    state = fields.Char("Estado")
    merged = fields.Boolean("Merged")
    merged_at = fields.Datetime("Merged At", help="Fecha/hora enviada por GitHub")
    merged_by = fields.Char("Merged by")
    base_branch = fields.Char("Base branch")
    head_branch = fields.Char("Head branch")
    merge_commit_sha = fields.Char("Merge commit SHA")
    labels = fields.Char("Labels (JSON)")
    assignees = fields.Char("Assignees (JSON)")
    requested_reviewers = fields.Char("Requested Reviewers (JSON)")

    body = fields.Text("Descripción (PR body)")
    raw_payload = fields.Text("Payload crudo (JSON)")