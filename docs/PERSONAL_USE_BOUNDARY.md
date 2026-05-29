# Personal Use Boundary

This project is a personal-use AI Agent platform.

The project is not intended to provide a public generative AI service by default. Public registration must remain disabled. User accounts must be created by an administrator or allowed through an explicit allowlist.

All Chat, Agent, and private API endpoints must require authentication. Hiding a button in the frontend is not access control; the backend must enforce permissions for every private action.

The default operating model is private personal use only:

- No public self-service registration.
- No anonymous Chat, Agent, or private API access.
- No default public API service.
- Accounts are created by an administrator or allowed by `ALLOWED_EMAILS`.
- `ENABLE_PUBLIC_REGISTER` must default to `false`.

If the project is later opened to other users, monetized, made available through public registration, or exposed as an API service, the project must be reassessed before launch for ICP filing, privacy policy, user terms, content safety, generative AI service filing or registration, algorithm filing, and related compliance requirements.

