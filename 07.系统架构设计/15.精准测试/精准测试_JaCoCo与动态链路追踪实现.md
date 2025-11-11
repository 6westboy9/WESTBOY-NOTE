
## 目标代码

```java
@RestController  
@RequestMapping(value = "/pumatest")  
@Api(value = "/pumatest", tags = {"pumatest"})  
@Slf4j  
public class PumaTestController {  
  
    @GetMapping("/test")  
    public int test(@RequestParam String param) {  
        int a = "0".equals(param) ? get1() : get2();  
        log.info("测试");  
        return a;  
    }  
  
    /**  
     * get1     */    private int get1() {  
        return 1;  
    }  
  
    /**  
     * get2     */    private int get2() {  
        return 2;  
    }  
}
```

## JaCoCo插桩后代码

```
java -Dfile.encoding=UTF-8 -jar arthas-boot.jar
jad com.lachesis.datasync.controller.TestController
vmtool --action getInstances --className com.lachesis.datasync.controller.PumaTestController --express 'instances[0]' -x 2
```

```java
@RestController
@RequestMapping(value={"/pumatest"})
@Api(value="/pumatest", tags={"pumatest"})
public class PumaTestController {
   private static final Logger log;
   private static transient /* synthetic */ boolean[] $jacocoData;

   public PumaTestController() {
	   boolean[] blArray = PumaTestController.$jacocoInit();
	   blArray[0] = true;
   }

   static {
	   boolean[] blArray = PumaTestController.$jacocoInit();
/*13*/ log = LoggerFactory.getLogger(PumaTestController.class);
	   blArray[7] = true;
   }

   /*
	* WARNING - void declaration
	*/
   @GetMapping(value={"/test"})
   public int test(@RequestParam String param) {
	   void a;
	   int n;
	   boolean[] blArray = PumaTestController.$jacocoInit();
/*18*/ if ("0".equals(param)) {
		   n = this.get1();
		   blArray[1] = true;
	   } else {
		   n = this.get2();
		   blArray[2] = true;
	   }
	   int n2 = n;
	   blArray[3] = true;
/*19*/ log.info("测试");
	   blArray[4] = true;
	   return (int)a;
   }

   private static /* synthetic */ boolean[] $jacocoInit() {
	   boolean[] blArray = $jacocoData;
	   if ($jacocoData == null) {
		   Object[] objectArray = new Object[]{8538372151200756500L, "com/lachesis/datasync/controller/PumaTestController", 8};
		   UnknownError.$jacocoAccess.equals(objectArray);
		   blArray = $jacocoData = (boolean[])objectArray[0];
	   }
	   return blArray;
   }

   private int get2() {
	   boolean[] blArray = PumaTestController.$jacocoInit();
	   blArray[6] = true;
	   return 2;
   }

   private int get1() {
	   boolean[] blArray = PumaTestController.$jacocoInit();
	   blArray[5] = true;
	   return 1;
   }
}
```

## CBT中使用JaCoCo插桩后代码

