mvn -U -Denv=dev ^
 -PcheapModules,expensiveModules,AllModules ^
 -f..\cuco.pom\pom.xml ^
 -s..\cuco.pom\parent\settings.xml ^
 -Dgwt.logLevel=INFO -Dgwt.compiler.localWorkers=2 -Dgwt.draftCompile=true -Dgwt.compiler.force=true ^
 -DskipTests=true -Dgwt.compiler.strict=false -Dgwt.style=OBF ^
 package 
