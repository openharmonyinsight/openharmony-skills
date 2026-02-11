# ArkTS Annotations Reference

## Annotation Declaration

```typescript
@AnnotationMeta
annotation AnnotationName(params?: string) {
  // Annotation body (optional)
}
```

---

## @Retention Meta-Annotation

Defines annotation retention policy:

```typescript
@Retention(RetentionPolicy.RUNTIME)
annotation MyRuntimeAnnotation {}

@Retention(RetentionPolicy.SOURCE)
annotation MySourceAnnotation {}
```

---

## @Target Meta-Annotation

Defines valid annotation targets:

```typescript
@Target(ElementType.CLASS)
annotation ClassOnly {}

@Target([ElementType.CLASS, ElementType.METHOD])
annotation ClassOrMethod {}
```

**Targets:**
- `ElementType.CLASS`
- `ElementType.METHOD`
- `ElementType.FIELD`
- `ElementType.PARAMETER`

---

## Using Annotations

### Class Annotation

```typescript
@Deprecated
@Author("John Doe")
class OldClass {}
```

### Method Annotation

```typescript
class Example {
  @Override
  public toString(): string {
    return "Example"
  }
}
```

### Field Annotation

```typescript
class Settings {
  @ReadOnly
  @DefaultValue("config.json")
  public configPath: string = "config.json"
}
```

### Parameter Annotation

```typescript
function log(
  @Description("Message to log") message: string
): void {
  console.log(message)
}
```

---

## Runtime Access

```typescript
@Retention(RetentionPolicy.RUNTIME)
annotation MyAnnotation(value: string)

@MyAnnotation("test")
class AnnotatedClass {}

// Reflection access (if supported)
let annotations: MyAnnotation[] = getAnnotations(AnnotatedClass)
```
