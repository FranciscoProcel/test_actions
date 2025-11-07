# -*- coding: utf-8 -*-
{
    "name": "Trescloud - GitHub Release Webhook",
    "summary": "Endpoint para recibir webhook de GitHub y registrar payloads",
    "version": "16.0.1.0.0",
    "author": "Trescloud",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/github_webhook_log_views.xml",
    ],
    "application": False,
    "installable": True,
}