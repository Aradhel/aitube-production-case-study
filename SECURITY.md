# Security Policy

## Reporting a vulnerability

Please report suspected security or privacy issues privately through the contact page at [aitubeapp.com/contact](https://aitubeapp.com/contact). Do not include passwords, payment information, private API credentials, or unrelated personal data in the first message.

Please do not open a public issue for a vulnerability that could expose user media, account data, billing state, infrastructure, or service credentials.

## Public repository boundary

This repository contains documentation only. It must never contain:

- `.env` files or credential exports
- API, OAuth, billing, email, storage, or GPU-provider secrets
- Production or local user databases
- User uploads or generated customer media
- Application logs, render caches, or analytics exports
- Private IP addresses, SSH material, or infrastructure inventories
- Proprietary production source code

## Responsible disclosure

When reporting a problem, include:

- A concise description of the issue
- The affected public page or workflow
- Reproduction steps using non-sensitive test data
- The observed and expected behavior
- Any potential impact

Avoid accessing other users' data, disrupting rendering capacity, or testing payment flows with unauthorized instruments.
