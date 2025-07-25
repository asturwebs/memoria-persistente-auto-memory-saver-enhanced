# Política de Seguridad - Memoria Persistente (Auto Memory Saver Enhanced)

## 🔒 Versiones Soportadas

| Versión | Soporte de Seguridad |
| ------- | ------------------- |
| 2.1.x   | ✅ Sí               |
| 2.0.x   | ✅ Sí               |
| < 2.0   | ❌ No               |

## 🚨 Reportar Vulnerabilidades

Si descubres una vulnerabilidad de seguridad, por favor **NO** la reportes públicamente. En su lugar:

### Proceso de Reporte Responsable

1. **Email Privado**: Envía los detalles a pedro@asturwebs.es
2. **Información Requerida**:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducir
   - Impacto potencial
   - Versión afectada
   - Cualquier mitigación conocida

3. **Respuesta Esperada**:
   - Confirmación de recepción: 24-48 horas
   - Evaluación inicial: 1 semana
   - Resolución: Según severidad (1-4 semanas)

### Severidad de Vulnerabilidades

- **Crítica**: Ejecución remota de código, acceso no autorizado a datos
- **Alta**: Escalación de privilegios, bypass de autenticación
- **Media**: Divulgación de información, DoS
- **Baja**: Problemas menores de configuración

## 🛡️ Mejores Prácticas de Seguridad

### Para Usuarios
- Mantén OpenWebUI actualizado
- Revisa las configuraciones de válvulas regularmente
- No compartas logs que contengan información sensible
- Usa el modo privado para conversaciones sensibles

### Para Desarrolladores
- Valida todas las entradas de usuario
- Sanitiza datos antes de almacenar
- Usa logging seguro (sin datos sensibles)
- Implementa rate limiting apropiado

## 🔐 Consideraciones de Privacidad

- Las memorias se almacenan localmente en OpenWebUI
- No se envían datos a servicios externos
- El modo privado previene el guardado de memorias
- Los logs pueden contener fragmentos de conversación (configurar apropiadamente)

## 📋 Auditorías de Seguridad

- Revisión de código regular
- Análisis de dependencias
- Testing de penetración básico
- Monitoreo de vulnerabilidades conocidas

## 🤝 Divulgación Coordinada

Trabajamos con investigadores de seguridad para:
- Validar y reproducir reportes
- Desarrollar patches de manera responsable
- Coordinar la divulgación pública
- Reconocer contribuciones de seguridad

## 📞 Contacto de Seguridad

- **Email**: pedro@asturwebs.es
- **PGP**: Disponible bajo petición
- **Respuesta**: 24-48 horas para reportes críticos

¡Gracias por ayudar a mantener Auto Memory Saver Enhanced seguro! 🙏
