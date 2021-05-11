Hola a todas,

Os recuerdo que desde C.O. Contabilidad pedimos que las transferencias a Arterra se hagan de una forma determinada, tanto la gente de casa, como visitas o pagos de eventos. 
 
## Aquí los detalles de la cuenta: 

```
Nombre: Asociación Arterra Bizimodu
IBAN: ES97 1491 0001 2921 1057 3728
BIC: TRIOESMMXXX 
```

## Esta es la plantilla para poner en el concepto de pago:

```
AB1.Fuego.V:XXX.C:YYY.P:ZZZ.E:XXX.I:YYY.F:ZZZ.D:XXX.S:YYY.B:ZZZ
```

* Usar la plantilla es muy fácil si accedéis a vuestro banco online (os puedo ayudar si lo necesitáis). 
* Idealmente se podría establecer la vivienda/proyecto como transferencia periódica y lo demás se puede ir haciendo a mano mes a mes. 
* La mayoría de bancos también ofrecen la posibilidad de guardar una transferencia como favorita, de forma que no tengáis que recordar este código cada vez. 
* Podéis usar los elementos por separado o todos juntos en un mismo pago.
* Si queréis añadir algo porque lo necesitáis como concepto lo podéis añadir después del código separado por un espacio

## Notas sobre puntuación: 

* Nota 1: Fijaos que entre elementos no hay espacios sino que hay puntos.
* Nota 2: Los decimales en las cantidades se ponen con coma baja o alta: 32,50 o 32'50. No uséis punto por favor ya que se usa como separador (ni acento tampoco).
* Nota 3: En caso de que vuestro banco no admita comas "," o " ' ", evitad pagar cosas fraccionadas y redondead la cantidad
* Nota 4: los dos puntos después de la letra son opcionales en caso de que vuestro banco no permita ese carácter p.ej. 

```
AB1.Fuego.VXXX.CYYY.PZZZ.EXXX.IYYY.FZZZ.DXXX.SYYY.BZZZ
```

* Nota 5: si vuestro banco no os permite usar el punto "." podeis usar dos paréntesis "()". p. ej.  

```
AB1()Fuego()V:XXX()C:YYY()P:ZZZ()E:XXX()I:YYY()F:ZZZ()D:XXX()S:YYY()B:ZZZ
```

* Nota 6: las notas 4 y 5 son combinables :) p. ej. 

```
AB1()Fuego()VXXX()CYYY()PZZZ()EXXX()IYYY()FZZZ()DXXX()SYYY()BZZZ
```

## Notas sobre el significado de las letras: 

* **V** corresponde a cuotas de vivienda (va seguido de dos puntos (opcional) y la cantidad). A pagar hasta el dia 5 de cada mes en curso. Si tenéis más de un mes de deuda os corresponde poneros en contacto con C.O. Contabilidad para plantear un escenario de cómo se va a saldar esa deuda y cuando.
* **C** corresponde a cuotas de comedor (va seguido de dos puntos (opcional) y la cantidad). A pagar a mes vencido
* **P** corresponde a cuotas de proyecto emprendedor (va seguido de dos puntos (opcional) y la cantidad). A pagar hasta el dia 5 de cada mes en curso. 
Si tenéis más de un mes de deuda os corresponde poneros en contacto con C.O. Contabilidad para plantear un escenario de cómo se va a saldar esa deuda y cuando.
* **E** corresponde a cuotas de almuerzos (va seguido de dos puntos (opcional) y la cantidad). A pagar a mes vencido
* **I** corresponde a cuota de integración (va seguido de dos puntos (opcional) y la cantidad). A pagar por la gente que entra a integración. A acordar con Contabilidad la mejor manera de pagar si se quiere pagar a plazos
* **F** corresponde a fondo de solidaridad (va seguido de dos puntos (opcional) y la cantidad). Fondo de solidaridad puntual implantado en 2020. 
* **D** corresponde a una donación (va seguido de dos puntos (opcional) y la cantidad). Gracias de todo corazón :)
* **S** corresponde a visita participativa [vivienda] (va seguido de dos puntos (opcional) y la cantidad)
* **B** corresponde a bote [comedor de visitas] (va seguido de dos puntos (opcional) y la cantidad)

## Notas sobre pago de visitas participativas:
En el caso de visitas participativas podéis usar el fuego "Visita". Por ejemplo:
```
AB1.Visita.S:100.B:12,5
```

## Notas sobre pago de encuentros:
En el caso de encuentros no hace falta usar el código ab1. 
Sí que pedimos que C.O. Coordinación de Centro de Encuentros defina un nombre fijo del evento p.ej. "facilitación abril 21".
Las personas que paguen a través de banco lo hagan poniendo en el concepto: 

```
"Encuentro Arterra [nombre evento]" 
```
por ejemplo:

```
Encuentro Arterra facilitación abril 21
```

Antes y después se pueden añadir más cosas en el concepto p.ej.
```
Encuentro Arterra facilitación abril 21 Juan Palomo
```

## Ejemplos:

* ```AB1.Angel.V:300.E:20.F:60```
* ```AB1.montxo-lide.C:46 mensaje que necesitan montxo y lide```
* ```AB1.Ana.V:282.P:50```
* ```AB1.Mauge.V:250.C:50.P:20```
* ```AB1.Valen.V:250.C:40.F:60```
* ```AB1.monica-franco.B:30 Comidas visitas```
* ```AB1.Peppe.D:67```
* ```AB1.Visita.S:100.B:12,5* Encuentro Arterra facilitación abril 21 Juan Palomo```