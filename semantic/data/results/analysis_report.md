# Semantic Code Analysis Report

## Statistics
- Total Artifacts: 54
- Number of Clusters: 10

## Cluster Details

### Cluster 3
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### build-impl.xml
- build-impl.xml
  - Description: Code from programlisting
  - Source Code:
```java
<?xmlversion="1.0"encoding="UTF-8"?>
<!--
***GENERATEDFROMproject.xml-DONOTEDIT***
***EDIT../build.xmlINSTEAD***

Forthepurposeofeasierreadingthescript
isdividedintofollowingsections:
-initialization
-compilation
-dist
-execution
-debugging
-javadoc
-testcompilation
-testexecution
-testdebugging
-cleanup

-->
<projectxmlns:webproject1="http://www.netbeans.org/ns/web-project/1"xmlns:webproject2="http://www.netbeans.org/ns/web-project/2"xmlns:webproject3="http://www.netbeans.org/ns/web-project/3"basedir=".."default="default"name="HospitalManagementSystem-impl">
<importfile="ant-deploy.xml"/>
<failmessage="PleasebuildusingAnt1.7.1orhigher.">
<condition>
<not>
<antversionatleast="1.7.1"/>
</not>
</condition>
</fail>
<targetdepends="dist,javadoc"description="Buildwholeproject."name="default"/>
<!--
INITIALIZATIONSECTION
-->
<targetname="-pre-init">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="-pre-init"name="-init-private">
<propertyfile="nbproject/private/private.properties"/>
</target>
<targetdepends="-pre-init,-init-private"name="-init-user">
<propertyfile="${user.properties.file}"/>
<!--Thetwopropertiesbelowareusuallyoverridden-->
<!--bytheactiveplatform.Justafallback.-->
<propertyname="default.javac.source"value="1.4"/>
<propertyname="default.javac.target"value="1.4"/>
</target>
<targetdepends="-pre-init,-init-private,-init-user"name="-init-project">
<propertyfile="nbproject/project.properties"/>
</target>
<targetdepends="-pre-init,-init-private,-init-user,-init-project,-init-macrodef-property"if="dist.ear.dir"name="-do-ear-init"/>
<targetdepends="-pre-init,-init-private,-init-user,-init-project,-init-macrodef-property"name="-do-init">
<conditionproperty="have.tests">
<or>
<availablefile="${test.src.dir}"/>
</or>
</condition>
<conditionproperty="have.sources">
<or>
<availablefile="${src.dir}"/>
</or>
</condition>
<conditionproperty="netbeans.home+have.tests">
<and>
<issetproperty="netbeans.home"/>
<issetproperty="have.tests"/>
</and>
</condition>
<conditionproperty="no.javadoc.preview">
<isfalsevalue="${javadoc.preview}"/>
</condition>
<propertyname="javac.compilerargs"value=""/>
<conditionproperty="no.deps">
<and>
<istruevalue="${no.dependencies}"/>
</and>
</condition>
<conditionproperty="no.dist.ear.dir">
<not>
<issetproperty="dist.ear.dir"/>
</not>
</condition>
<propertyname="build.web.excludes"value="${build.classes.excludes}"/>
<conditionproperty="do.compile.jsps">
<istruevalue="${compile.jsps}"/>
</condition>
<conditionproperty="do.debug.server">
<or>
<not>
<issetproperty="debug.server"/>
</not>
<istruevalue="${debug.server}"/>
<and>
<not>
<istruevalue="${debug.server}"/>
</not>
<not>
<istruevalue="${debug.client}"/>
</not>
</and>
</or>
</condition>
<conditionproperty="do.debug.client">
<istruevalue="${debug.client}"/>
</condition>
<conditionproperty="do.display.browser">
<istruevalue="${display.browser}"/>
</condition>
<conditionproperty="do.display.browser.debug.old">
<and>
<issetproperty="do.display.browser"/>
<not>
<issetproperty="do.debug.client"/>
</not>
<not>
<issetproperty="browser.context"/>
</not>
</and>
</condition>
<conditionproperty="do.display.browser.debug">
<and>
<issetproperty="do.display.browser"/>
<not>
<issetproperty="do.debug.client"/>
</not>
<issetproperty="browser.context"/>
</and>
</condition>
<availablefile="${conf.dir}/MANIFEST.MF"property="has.custom.manifest"/>
<availablefile="${persistence.xml.dir}/persistence.xml"property="has.persistence.xml"/>
<conditionproperty="do.war.package.with.custom.manifest">
<issetproperty="has.custom.manifest"/>
</condition>
<conditionproperty="do.war.package.without.custom.manifest">
<not>
<issetproperty="has.custom.manifest"/>
</not>
</condition>
<conditionproperty="do.tmp.war.package.with.custom.manifest">
<and>
<issetproperty="has.custom.manifest"/>
<or>
<isfalsevalue="${directory.deployment.supported}"/>
<issetproperty="dist.ear.dir"/>
</or>
</and>
</condition>
<conditionproperty="do.tmp.war.package.without.custom.manifest">
<and>
<not>
<issetproperty="has.custom.manifest"/>
</not>
<or>
<isfalsevalue="${directory.deployment.supported}"/>
<issetproperty="dist.ear.dir"/>
</or>
</and>
</condition>
<conditionproperty="do.tmp.war.package">
<or>
<isfalsevalue="${directory.deployment.supported}"/>
<issetproperty="dist.ear.dir"/>
</or>
</condition>
<propertyname="build.meta.inf.dir"value="${build.web.dir}/META-INF"/>
<conditionelse=""property="application.args.param"value="${application.args}">
<and>
<issetproperty="application.args"/>
<not>
<equalsarg1="${application.args}"arg2=""trim="true"/>
</not>
</and>
</condition>
<propertyname="source.encoding"value="${file.encoding}"/>
<conditionproperty="javadoc.encoding.used"value="${javadoc.encoding}">
<and>
<issetproperty="javadoc.encoding"/>
<not>
<equalsarg1="${javadoc.encoding}"arg2=""/>
</not>
</and>
</condition>
<propertyname="javadoc.encoding.used"value="${source.encoding}"/>
<propertyname="includes"value="**"/>
<propertyname="excludes"value=""/>
<propertyname="runmain.jvmargs"value=""/>
<pathid="endorsed.classpath.path"path="${endorsed.classpath}"/>
<conditionelse=""property="endorsed.classpath.cmd.line.arg"value="-Xbootclasspath/p:'${toString:endorsed.classpath.path}'">
<and>
<issetproperty="endorsed.classpath"/>
<lengthlength="0"string="${endorsed.classpath}"when="greater"/>
</and>
</condition>
<conditionelse="false"property="jdkBug6558476">
<and>
<matchespattern="1\.[56]"string="${java.specification.version}"/>
<not>
<osfamily="unix"/>
</not>
</and>
</condition>
<propertyname="javac.fork"value="${jdkBug6558476}"/>
<conditionproperty="junit.available">
<or>
<availableclassname="org.junit.Test"classpath="${run.test.classpath}"/>
<availableclassname="junit.framework.Test"classpath="${run.test.classpath}"/>
</or>
</condition>
<conditionproperty="testng.available">
<availableclassname="org.testng.annotations.Test"classpath="${run.test.classpath}"/>
</condition>
<conditionproperty="junit+testng.available">
<and>
<istruevalue="${junit.available}"/>
<istruevalue="${testng.available}"/>
</and>
</condition>
<conditionelse="testng"property="testng.mode"value="mixed">
<istruevalue="${junit+testng.available}"/>
</condition>
<conditionelse=""property="testng.debug.mode"value="-mixed">
<istruevalue="${junit+testng.available}"/>
</condition>
</target>
<targetdepends="init"name="-init-cos"unless="deploy.on.save">
<conditionproperty="deploy.on.save"value="true">
<or>
<istruevalue="${j2ee.deploy.on.save}"/>
<istruevalue="${j2ee.compile.on.save}"/>
</or>
</condition>
</target>
<targetname="-post-init">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="-pre-init,-init-private,-init-user,-init-project,-do-init"name="-init-check">
<failunless="src.dir">Mustsetsrc.dir</fail>
<failunless="test.src.dir">Mustsettest.src.dir</fail>
<failunless="build.dir">Mustsetbuild.dir</fail>
<failunless="build.web.dir">Mustsetbuild.web.dir</fail>
<failunless="build.generated.dir">Mustsetbuild.generated.dir</fail>
<failunless="dist.dir">Mustsetdist.dir</fail>
<failunless="build.classes.dir">Mustsetbuild.classes.dir</fail>
<failunless="dist.javadoc.dir">Mustsetdist.javadoc.dir</fail>
<failunless="build.test.classes.dir">Mustsetbuild.test.classes.dir</fail>
<failunless="build.test.results.dir">Mustsetbuild.test.results.dir</fail>
<failunless="build.classes.excludes">Mustsetbuild.classes.excludes</fail>
<failunless="dist.war">Mustsetdist.war</fail>
<conditionproperty="missing.j2ee.server.home">
<and>
<matchespattern="j2ee.server.home"string="${j2ee.platform.classpath}"/>
<not>
<issetproperty="j2ee.server.home"/>
</not>
</and>
</condition>
<failif="missing.j2ee.server.home">
TheJavaEEserverclasspathisnotcorrectlysetup-serverhomedirectoryismissing.
EitheropentheprojectintheIDEandassigntheserverorsetuptheserverclasspathmanually.
Forexamplelikethis:
ant-Dj2ee.server.home=&lt;app_server_installation_directory&gt;
</fail>
<failunless="j2ee.platform.classpath">
TheJavaEEserverclasspathisnotcorrectlysetup.Youractiveservertypeis${j2ee.server.type}.
EitheropentheprojectintheIDEandassigntheserverorsetuptheserverclasspathmanually.
Forexamplelikethis:
ant-Duser.properties.file=&lt;path_to_property_file&gt;(whereyouputtheproperty"j2ee.platform.classpath"ina.propertiesfile)
orant-Dj2ee.platform.classpath=&lt;server_classpath&gt;(wherenopropertiesfileisused)
</fail>
</target>
<targetname="-init-macrodef-property">
<macrodefname="property"uri="http://www.netbeans.org/ns/web-project/1">
<attributename="name"/>
<attributename="value"/>
<sequential>
<propertyname="{name}"value="${{value}}"/>
</sequential>
</macrodef>
</target>
<targetdepends="-init-ap-cmdline-properties"if="ap.supported.internal"name="-init-macrodef-javac-with-processors">
<macrodefname="javac"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${src.dir}"name="srcdir"/>
<attributedefault="${build.classes.dir}"name="destdir"/>
<attributedefault="${javac.classpath}:${j2ee.platform.classpath}"name="classpath"/>
<attributedefault="${javac.processorpath}"name="processorpath"/>
<attributedefault="${build.generated.sources.dir}/ap-source-output"name="apgeneratedsrcdir"/>
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="${javac.debug}"name="debug"/>
<attributedefault="${empty.dir}"name="gensrcdir"/>
<elementname="customize"optional="true"/>
<sequential>
<propertylocation="${build.dir}/empty"name="empty.dir"/>
<mkdirdir="${empty.dir}"/>
<mkdirdir="{apgeneratedsrcdir}"/>
<javacdebug="{debug}"deprecation="${javac.deprecation}"destdir="{destdir}"encoding="${source.encoding}"excludes="{excludes}"fork="${javac.fork}"includeantruntime="false"includes="{includes}"source="${javac.source}"srcdir="{srcdir}"target="${javac.target}">
<src>
<dirsetdir="{gensrcdir}"erroronmissingdir="false">
<includename="*"/>
</dirset>
</src>
<classpath>
<pathpath="{classpath}"/>
</classpath>
<compilerargline="${endorsed.classpath.cmd.line.arg}"/>
<compilerargline="${javac.compilerargs}"/>
<compilerargvalue="-processorpath"/>
<compilerargpath="{processorpath}:${empty.dir}"/>
<compilerargline="${ap.processors.internal}"/>
<compilerargvalue="-s"/>
<compilerargpath="{apgeneratedsrcdir}"/>
<compilerargline="${ap.proc.none.internal}"/>
<customize/>
</javac>
</sequential>
</macrodef>
</target>
<targetdepends="-init-ap-cmdline-properties"name="-init-macrodef-javac-without-processors"unless="ap.supported.internal">
<macrodefname="javac"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${src.dir}"name="srcdir"/>
<attributedefault="${build.classes.dir}"name="destdir"/>
<attributedefault="${javac.classpath}:${j2ee.platform.classpath}"name="classpath"/>
<attributedefault="${javac.processorpath}"name="processorpath"/>
<attributedefault="${build.generated.sources.dir}/ap-source-output"name="apgeneratedsrcdir"/>
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="${javac.debug}"name="debug"/>
<attributedefault="${empty.dir}"name="gensrcdir"/>
<elementname="customize"optional="true"/>
<sequential>
<propertylocation="${build.dir}/empty"name="empty.dir"/>
<mkdirdir="${empty.dir}"/>
<javacdebug="{debug}"deprecation="${javac.deprecation}"destdir="{destdir}"encoding="${source.encoding}"excludes="{excludes}"includeantruntime="false"includes="{includes}"source="${javac.source}"srcdir="{srcdir}"target="${javac.target}">
<src>
<dirsetdir="{gensrcdir}"erroronmissingdir="false">
<includename="*"/>
</dirset>
</src>
<classpath>
<pathpath="{classpath}"/>
</classpath>
<compilerargline="${endorsed.classpath.cmd.line.arg}"/>
<compilerargline="${javac.compilerargs}"/>
<customize/>
</javac>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-javac-with-processors,-init-macrodef-javac-without-processors"name="-init-macrodef-javac">
<macrodefname="depend"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${src.dir}"name="srcdir"/>
<attributedefault="${build.classes.dir}"name="destdir"/>
<attributedefault="${javac.classpath}:${j2ee.platform.classpath}"name="classpath"/>
<sequential>
<dependcache="${build.dir}/depcache"destdir="{destdir}"excludes="${excludes}"includes="${includes}"srcdir="{srcdir}">
<classpath>
<pathpath="{classpath}"/>
</classpath>
</depend>
</sequential>
</macrodef>
<macrodefname="force-recompile"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${build.classes.dir}"name="destdir"/>
<sequential>
<failunless="javac.includes">Mustsetjavac.includes</fail>
<pathconvertpathsep="${line.separator}"property="javac.includes.binary">
<path>
<filelistdir="{destdir}"files="${javac.includes}"/>
</path>
<globmapperfrom="*.java"to="*.class"/>
</pathconvert>
<tempfiledeleteonexit="true"property="javac.includesfile.binary"/>
<echofile="${javac.includesfile.binary}"message="${javac.includes.binary}"/>
<delete>
<filesincludesfile="${javac.includesfile.binary}"/>
</delete>
<deletefile="${javac.includesfile.binary}"/>
</sequential>
</macrodef>
</target>
<targetif="${junit.available}"name="-init-macrodef-junit-init">
<conditionelse="false"property="nb.junit.batch"value="true">
<and>
<istruevalue="${junit.available}"/>
<not>
<issetproperty="test.method"/>
</not>
</and>
</condition>
<conditionelse="false"property="nb.junit.single"value="true">
<and>
<istruevalue="${junit.available}"/>
<issetproperty="test.method"/>
</and>
</condition>
</target>
<targetname="-init-test-properties">
<propertyname="test.binaryincludes"value="&lt;nothing&gt;"/>
<propertyname="test.binarytestincludes"value=""/>
<propertyname="test.binaryexcludes"value=""/>
</target>
<targetif="${nb.junit.single}"name="-init-macrodef-junit-single"unless="${nb.junit.batch}">
<macrodefname="junit"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementname="customize"optional="true"/>
<sequential>
<junitdir="${basedir}"errorproperty="tests.failed"failureproperty="tests.failed"fork="true"showoutput="true"tempdir="${java.io.tmpdir}">
<testmethods="{testmethods}"name="{testincludes}"todir="${build.test.results.dir}"/>
<syspropertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<formattertype="brief"usefile="false"/>
<formattertype="xml"/>
<jvmargvalue="-ea"/>
<customize/>
</junit>
</sequential>
</macrodef>
</target>
<targetdepends="-init-test-properties"if="${nb.junit.batch}"name="-init-macrodef-junit-batch"unless="${nb.junit.single}">
<macrodefname="junit"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementname="customize"optional="true"/>
<sequential>
<propertyname="run.jvmargs.ide"value=""/>
<junitdir="${basedir}"errorproperty="tests.failed"failureproperty="tests.failed"fork="true"showoutput="true"tempdir="${build.dir}">
<batchtesttodir="${build.test.results.dir}">
<filesetdir="${test.src.dir}"excludes="{excludes},${excludes}"includes="{includes}">
<filenamename="{testincludes}"/>
</fileset>
<filesetdir="${build.test.classes.dir}"excludes="{excludes},${excludes},${test.binaryexcludes}"includes="${test.binaryincludes}">
<filenamename="${test.binarytestincludes}"/>
</fileset>
</batchtest>
<syspropertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<formattertype="brief"usefile="false"/>
<formattertype="xml"/>
<jvmargvalue="-ea"/>
<jvmargline="${run.jvmargs.ide}"/>
<customize/>
</junit>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-junit-init,-init-macrodef-junit-single,-init-macrodef-junit-batch"if="${junit.available}"name="-init-macrodef-junit"/>
<targetif="${testng.available}"name="-init-macrodef-testng">
<macrodefname="testng"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementname="customize"optional="true"/>
<sequential>
<conditionelse=""property="testng.methods.arg"value="{testincludes}.{testmethods}">
<issetproperty="test.method"/>
</condition>
<unionid="test.set">
<filesetdir="${test.src.dir}"excludes="{excludes},**/*.xml,${excludes}"includes="{includes}">
<filenamename="{testincludes}"/>
</fileset>
</union>
<taskdefclassname="org.testng.TestNGAntTask"classpath="${run.test.classpath}"name="testng"/>
<testngclassfilesetref="test.set"failureProperty="tests.failed"listeners="org.testng.reporters.VerboseReporter"methods="${testng.methods.arg}"mode="${testng.mode}"outputdir="${build.test.results.dir}"suitename="HospitalManagementSystem"testname="TestNGtests"workingDir="${basedir}">
<xmlfilesetdir="${build.test.classes.dir}"includes="{testincludes}"/>
<propertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</propertyset>
<customize/>
</testng>
</sequential>
</macrodef>
</target>
<targetname="-init-macrodef-test-impl">
<macrodefname="test-impl"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementimplicit="true"name="customize"optional="true"/>
<sequential>
<echo>Notestsexecuted.</echo>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-junit"if="${junit.available}"name="-init-macrodef-junit-impl">
<macrodefname="test-impl"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementimplicit="true"name="customize"optional="true"/>
<sequential>
<webproject2:junitexcludes="{excludes}"includes="{includes}"testincludes="{testincludes}"testmethods="{testmethods}">
<customize/>
</webproject2:junit>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-testng"if="${testng.available}"name="-init-macrodef-testng-impl">
<macrodefname="test-impl"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementimplicit="true"name="customize"optional="true"/>
<sequential>
<webproject2:testngexcludes="{excludes}"includes="{includes}"testincludes="{testincludes}"testmethods="{testmethods}">
<customize/>
</webproject2:testng>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-test-impl,-init-macrodef-junit-impl,-init-macrodef-testng-impl"name="-init-macrodef-test">
<macrodefname="test"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<sequential>
<webproject2:test-implexcludes="{excludes}"includes="{includes}"testincludes="{testincludes}"testmethods="{testmethods}">
<customize>
<classpath>
<pathpath="${run.test.classpath}:${j2ee.platform.classpath}:${j2ee.platform.embeddableejb.classpath}"/>
</classpath>
<jvmargline="${endorsed.classpath.cmd.line.arg}"/>
<jvmargline="${runmain.jvmargs}"/>
</customize>
</webproject2:test-impl>
</sequential>
</macrodef>
</target>
<targetif="${junit.available}"name="-init-macrodef-junit-debug"unless="${nb.junit.batch}">
<macrodefname="junit-debug"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementname="customize"optional="true"/>
<sequential>
<junitdir="${basedir}"errorproperty="tests.failed"failureproperty="tests.failed"fork="true"showoutput="true"tempdir="${java.io.tmpdir}">
<testmethods="{testmethods}"name="{testincludes}"todir="${build.test.results.dir}"/>
<syspropertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<formattertype="brief"usefile="false"/>
<formattertype="xml"/>
<jvmargvalue="-ea"/>
<jvmargline="${debug-args-line}"/>
<jvmargvalue="-Xrunjdwp:transport=${debug-transport},address=${jpda.address}"/>
<customize/>
</junit>
</sequential>
</macrodef>
</target>
<targetdepends="-init-test-properties"if="${nb.junit.batch}"name="-init-macrodef-junit-debug-batch">
<macrodefname="junit-debug"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementname="customize"optional="true"/>
<sequential>
<propertyname="run.jvmargs.ide"value=""/>
<junitdir="${basedir}"errorproperty="tests.failed"failureproperty="tests.failed"fork="true"showoutput="true"tempdir="${build.dir}">
<batchtesttodir="${build.test.results.dir}">
<filesetdir="${test.src.dir}"excludes="{excludes},${excludes}"includes="{includes}">
<filenamename="{testincludes}"/>
</fileset>
<filesetdir="${build.test.classes.dir}"excludes="{excludes},${excludes},${test.binaryexcludes}"includes="${test.binaryincludes}">
<filenamename="${test.binarytestincludes}"/>
</fileset>
</batchtest>
<syspropertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<formattertype="brief"usefile="false"/>
<formattertype="xml"/>
<jvmargvalue="-ea"/>
<jvmargline="${run.jvmargs.ide}"/>
<jvmargline="${debug-args-line}"/>
<jvmargvalue="-Xrunjdwp:transport=${debug-transport},address=${jpda.address}"/>
<customize/>
</junit>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-junit-debug,-init-macrodef-junit-debug-batch"if="${junit.available}"name="-init-macrodef-junit-debug-impl">
<macrodefname="test-debug-impl"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<elementimplicit="true"name="customize"optional="true"/>
<sequential>
<webproject2:junit-debugexcludes="{excludes}"includes="{includes}"testincludes="{testincludes}"testmethods="{testmethods}">
<customize/>
</webproject2:junit-debug>
</sequential>
</macrodef>
</target>
<targetif="${testng.available}"name="-init-macrodef-testng-debug">
<macrodefname="testng-debug"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${main.class}"name="testClass"/>
<attributedefault=""name="testMethod"/>
<elementname="customize2"optional="true"/>
<sequential>
<conditionelse="-testclass{testClass}"property="test.class.or.method"value="-methods{testClass}.{testMethod}">
<issetproperty="test.method"/>
</condition>
<conditionelse="-suitenameHospitalManagementSystem-testname{testClass}${test.class.or.method}"property="testng.cmd.args"value="{testClass}">
<matchespattern=".*\.xml"string="{testClass}"/>
</condition>
<deletedir="${build.test.results.dir}"quiet="true"/>
<mkdirdir="${build.test.results.dir}"/>
<webproject1:debugargs="${testng.cmd.args}"classname="org.testng.TestNG"classpath="${debug.test.classpath}:${j2ee.platform.embeddableejb.classpath}">
<customize>
<customize2/>
<jvmargvalue="-ea"/>
<argline="${testng.debug.mode}"/>
<argline="-d${build.test.results.dir}"/>
<argline="-listenerorg.testng.reporters.VerboseReporter"/>
</customize>
</webproject1:debug>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-testng-debug"if="${testng.available}"name="-init-macrodef-testng-debug-impl">
<macrodefname="testng-debug-impl"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${main.class}"name="testClass"/>
<attributedefault=""name="testMethod"/>
<elementimplicit="true"name="customize2"optional="true"/>
<sequential>
<webproject2:testng-debugtestClass="{testClass}"testMethod="{testMethod}">
<customize2/>
</webproject2:testng-debug>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-junit-debug-impl"if="${junit.available}"name="-init-macrodef-test-debug-junit">
<macrodefname="test-debug"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<attributedefault="${main.class}"name="testClass"/>
<attributedefault=""name="testMethod"/>
<sequential>
<webproject2:test-debug-implexcludes="{excludes}"includes="{includes}"testincludes="{testincludes}"testmethods="{testmethods}">
<customize>
<classpath>
<pathpath="${run.test.classpath}:${j2ee.platform.classpath}:${j2ee.platform.embeddableejb.classpath}"/>
</classpath>
<jvmargline="${endorsed.classpath.cmd.line.arg}"/>
<jvmargline="${runmain.jvmargs}"/>
</customize>
</webproject2:test-debug-impl>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-testng-debug-impl"if="${testng.available}"name="-init-macrodef-test-debug-testng">
<macrodefname="test-debug"uri="http://www.netbeans.org/ns/web-project/2">
<attributedefault="${includes}"name="includes"/>
<attributedefault="${excludes}"name="excludes"/>
<attributedefault="**"name="testincludes"/>
<attributedefault=""name="testmethods"/>
<attributedefault="${main.class}"name="testClass"/>
<attributedefault=""name="testMethod"/>
<sequential>
<webproject2:testng-debug-impltestClass="{testClass}"testMethod="{testMethod}">
<customize2>
<syspropertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
</customize2>
</webproject2:testng-debug-impl>
</sequential>
</macrodef>
</target>
<targetdepends="-init-macrodef-test-debug-junit,-init-macrodef-test-debug-testng"name="-init-macrodef-test-debug"/>
<targetname="-init-macrodef-java">
<macrodefname="java"uri="http://www.netbeans.org/ns/web-project/1">
<attributedefault="${main.class}"name="classname"/>
<attributedefault="${debug.classpath}"name="classpath"/>
<elementname="customize"optional="true"/>
<sequential>
<javaclassname="{classname}"fork="true">
<jvmargline="${endorsed.classpath.cmd.line.arg}"/>
<jvmargline="${runmain.jvmargs}"/>
<classpath>
<pathpath="{classpath}:${j2ee.platform.classpath}"/>
</classpath>
<syspropertyset>
<propertyrefprefix="run-sys-prop."/>
<mapperfrom="run-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<customize/>
</java>
</sequential>
</macrodef>
</target>
<targetname="-init-macrodef-nbjsdebug">
<macrodefname="nbjsdebugstart"uri="http://www.netbeans.org/ns/web-project/1">
<attributedefault="${client.url}"name="webUrl"/>
<sequential>
<nbjsdebugstarturlPart="${client.urlPart}"webUrl="{webUrl}"/>
</sequential>
</macrodef>
</target>
<targetdepends="-init-debug-args"name="-init-macrodef-nbjpda">
<macrodefname="nbjpdastart"uri="http://www.netbeans.org/ns/web-project/1">
<attributedefault="${main.class}"name="name"/>
<attributedefault="${debug.classpath}:${j2ee.platform.classpath}"name="classpath"/>
<sequential>
<nbjpdastartaddressproperty="jpda.address"name="{name}"transport="${debug-transport}">
<classpath>
<pathpath="{classpath}"/>
</classpath>
</nbjpdastart>
</sequential>
</macrodef>
<macrodefname="nbjpdareload"uri="http://www.netbeans.org/ns/web-project/1">
<attributedefault="${build.classes.dir}"name="dir"/>
<sequential>
<nbjpdareload>
<filesetdir="{dir}"includes="${fix.classes}">
<includename="${fix.includes}*.class"/>
</fileset>
</nbjpdareload>
</sequential>
</macrodef>
<macrodefname="nbjpdaappreloaded"uri="http://www.netbeans.org/ns/web-project/1">
<sequential>
<nbjpdaappreloaded/>
</sequential>
</macrodef>
</target>
<targetname="-init-debug-args">
<propertyname="version-output"value="javaversion&quot;${ant.java.version}"/>
<conditionproperty="have-jdk-older-than-1.4">
<or>
<containsstring="${version-output}"substring="javaversion&quot;1.0"/>
<containsstring="${version-output}"substring="javaversion&quot;1.1"/>
<containsstring="${version-output}"substring="javaversion&quot;1.2"/>
<containsstring="${version-output}"substring="javaversion&quot;1.3"/>
</or>
</condition>
<conditionelse="-Xdebug"property="debug-args-line"value="-Xdebug-Xnoagent-Djava.compiler=none">
<istruevalue="${have-jdk-older-than-1.4}"/>
</condition>
<conditionelse="dt_socket"property="debug-transport-by-os"value="dt_shmem">
<osfamily="windows"/>
</condition>
<conditionelse="${debug-transport-by-os}"property="debug-transport"value="${debug.transport}">
<issetproperty="debug.transport"/>
</condition>
</target>
<targetdepends="-init-debug-args"name="-init-macrodef-debug">
<macrodefname="debug"uri="http://www.netbeans.org/ns/web-project/1">
<attributedefault="${main.class}"name="classname"/>
<attributedefault="${debug.classpath}:${j2ee.platform.classpath}"name="classpath"/>
<attributedefault="${application.args.param}"name="args"/>
<elementname="customize"optional="true"/>
<sequential>
<javaclassname="{classname}"fork="true">
<jvmargline="${endorsed.classpath.cmd.line.arg}"/>
<jvmargline="${debug-args-line}"/>
<jvmargvalue="-Xrunjdwp:transport=${debug-transport},address=${jpda.address}"/>
<jvmargline="${runmain.jvmargs}"/>
<classpath>
<pathpath="{classpath}"/>
</classpath>
<syspropertyset>
<propertyrefprefix="run-sys-prop."/>
<mapperfrom="run-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<argline="{args}"/>
<customize/>
</java>
</sequential>
</macrodef>
</target>
<targetname="-init-taskdefs">
<failunless="libs.CopyLibs.classpath">
Thelibs.CopyLibs.classpathpropertyisnotsetup.
Thispropertymustpointto
org-netbeans-modules-java-j2seproject-copylibstask.jarfilewhichispart
ofNetBeansIDEinstallationandisusuallylocatedat
&lt;netbeans_installation&gt;/java&lt;version&gt;/ant/extrafolder.
EitheropentheprojectintheIDEandmakesureCopyLibslibrary
existsorsetupthepropertymanually.Forexamplelikethis:
ant-Dlibs.CopyLibs.classpath=a/path/to/org-netbeans-modules-java-j2seproject-copylibstask.jar
</fail>
<taskdefclasspath="${libs.CopyLibs.classpath}"resource="org/netbeans/modules/java/j2seproject/copylibstask/antlib.xml"/>
</target>
<targetname="-init-ap-cmdline-properties">
<propertyname="annotation.processing.enabled"value="true"/>
<propertyname="annotation.processing.processors.list"value=""/>
<propertyname="annotation.processing.run.all.processors"value="true"/>
<propertyname="javac.processorpath"value="${javac.classpath}"/>
<propertyname="javac.test.processorpath"value="${javac.test.classpath}"/>
<conditionproperty="ap.supported.internal"value="true">
<not>
<matchespattern="1\.[0-5](\..*)?"string="${javac.source}"/>
</not>
</condition>
</target>
<targetdepends="-init-ap-cmdline-properties"if="ap.supported.internal"name="-init-ap-cmdline-supported">
<conditionelse=""property="ap.processors.internal"value="-processor${annotation.processing.processors.list}">
<isfalsevalue="${annotation.processing.run.all.processors}"/>
</condition>
<conditionelse=""property="ap.proc.none.internal"value="-proc:none">
<isfalsevalue="${annotation.processing.enabled}"/>
</condition>
</target>
<targetdepends="-init-ap-cmdline-properties,-init-ap-cmdline-supported"name="-init-ap-cmdline">
<propertyname="ap.cmd.line.internal"value=""/>
</target>
<!--
preNB7.2profilingsection;consideritdeprecated
-->
<targetdepends="-profile-pre-init,init,-profile-post-init,-profile-init-check"if="profiler.info.jvmargs.agent"name="profile-init"/>
<targetif="profiler.info.jvmargs.agent"name="-profile-pre-init">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetif="profiler.info.jvmargs.agent"name="-profile-post-init">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="-profile-pre-init,init,-profile-post-init"if="profiler.info.jvmargs.agent"name="-profile-init-check">
<failunless="profiler.info.jvm">MustsetJVMtouseforprofilinginprofiler.info.jvm</fail>
<failunless="profiler.info.jvmargs.agent">MustsetprofileragentJVMargumentsinprofiler.info.jvmargs.agent</fail>
</target>
<!--
endofpreNB7.2profilingsection
-->
<targetdepends="-pre-init,-init-private,-init-user,-init-project,-do-init,-post-init,-init-check,-init-macrodef-property,-init-macrodef-javac,-init-macrodef-test,-init-macrodef-test-debug,-init-macrodef-java,-init-macrodef-nbjpda,-init-macrodef-nbjsdebug,-init-macrodef-debug,-init-taskdefs,-init-ap-cmdline"name="init"/>
<!--
COMPILATIONSECTION
-->
<targetdepends="init"if="no.dist.ear.dir"name="deps-module-jar"unless="no.deps"/>
<targetdepends="init"if="dist.ear.dir"name="deps-ear-jar"unless="no.deps"/>
<targetdepends="init,deps-module-jar,deps-ear-jar"name="deps-jar"unless="no.deps"/>
<targetdepends="init,deps-jar"name="-pre-pre-compile">
<mkdirdir="${build.classes.dir}"/>
</target>
<targetname="-pre-compile">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetname="-copy-webdir">
<copytodir="${build.web.dir}">
<filesetdir="${web.docbase.dir}"excludes="${build.web.excludes},${excludes}"includes="${includes}"/>
</copy>
<copytodir="${build.web.dir}/WEB-INF">
<filesetdir="${webinf.dir}"excludes="${build.web.excludes}"/>
</copy>
</target>
<targetdepends="init,deps-jar,-pre-pre-compile,-pre-compile,-copy-manifest,-copy-persistence-xml,-copy-webdir,library-inclusion-in-archive,library-inclusion-in-manifest"if="have.sources"name="-do-compile">
<webproject2:javacdestdir="${build.classes.dir}"gensrcdir="${build.generated.sources.dir}"/>
<copytodir="${build.classes.dir}">
<filesetdir="${src.dir}"excludes="${build.classes.excludes},${excludes}"includes="${includes}"/>
</copy>
</target>
<targetif="has.custom.manifest"name="-copy-manifest">
<mkdirdir="${build.meta.inf.dir}"/>
<copytodir="${build.meta.inf.dir}">
<filesetdir="${conf.dir}"includes="MANIFEST.MF"/>
</copy>
</target>
<targetif="has.persistence.xml"name="-copy-persistence-xml">
<mkdirdir="${build.web.dir}/WEB-INF/classes/META-INF"/>
<copytodir="${build.web.dir}/WEB-INF/classes/META-INF">
<filesetdir="${persistence.xml.dir}"includes="persistence.xmlorm.xml"/>
</copy>
</target>
<targetname="-post-compile">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,deps-jar,-pre-pre-compile,-pre-compile,-do-compile,-post-compile"description="Compileproject."name="compile"/>
<targetname="-pre-compile-single">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,deps-jar,-pre-pre-compile"name="-do-compile-single">
<failunless="javac.includes">MustselectsomefilesintheIDEorsetjavac.includes</fail>
<webproject2:javacexcludes=""gensrcdir="${build.generated.sources.dir}"includes="${javac.includes}"/>
<copytodir="${build.classes.dir}">
<filesetdir="${src.dir}"excludes="${build.classes.excludes},${excludes}"includes="${includes}"/>
</copy>
</target>
<targetname="-post-compile-single">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,deps-jar,-pre-pre-compile,-pre-compile-single,-do-compile-single,-post-compile-single"name="compile-single"/>
<propertyname="jspc.schemas"value="/resources/schemas/"/>
<propertyname="jspc.dtds"value="/resources/dtds/"/>
<targetdepends="compile"description="TestcompileJSPpagestoexposecompilationerrors."if="do.compile.jsps"name="compile-jsps">
<mkdirdir="${build.generated.dir}/src"/>
<javaclassname="org.netbeans.modules.web.project.ant.JspC"failonerror="true"fork="true">
<argvalue="-uriroot"/>
<argfile="${basedir}/${build.web.dir}"/>
<argvalue="-d"/>
<argfile="${basedir}/${build.generated.dir}/src"/>
<argvalue="-die1"/>
<argvalue="-schemas${jspc.schemas}"/>
<argvalue="-dtds${jspc.dtds}"/>
<argvalue="-compilerSourceVM${javac.source}"/>
<argvalue="-compilerTargetVM${javac.target}"/>
<argvalue="-javaEncoding${source.encoding}"/>
<argvalue="-sysClasspath${libs.jsp-compilation-syscp.classpath}"/>
<classpathpath="${java.home}/../lib/tools.jar:${libs.jsp-compiler.classpath}:${libs.jsp-compilation.classpath}"/>
</java>
<mkdirdir="${build.generated.dir}/classes"/>
<webproject2:javacclasspath="${build.classes.dir}:${libs.jsp-compilation.classpath}:${javac.classpath}:${j2ee.platform.classpath}"destdir="${build.generated.dir}/classes"srcdir="${build.generated.dir}/src"/>
</target>
<targetdepends="compile"if="jsp.includes"name="-do-compile-single-jsp">
<failunless="javac.jsp.includes">MustselectsomefilesintheIDEorsetjavac.jsp.includes</fail>
<mkdirdir="${build.generated.dir}/src"/>
<javaclassname="org.netbeans.modules.web.project.ant.JspCSingle"failonerror="true"fork="true">
<argvalue="-uriroot"/>
<argfile="${basedir}/${build.web.dir}"/>
<argvalue="-d"/>
<argfile="${basedir}/${build.generated.dir}/src"/>
<argvalue="-die1"/>
<argvalue="-schemas${jspc.schemas}"/>
<argvalue="-dtds${jspc.dtds}"/>
<argvalue="-sysClasspath${libs.jsp-compilation-syscp.classpath}"/>
<argvalue="-jspc.files"/>
<argpath="${jsp.includes}"/>
<argvalue="-compilerSourceVM${javac.source}"/>
<argvalue="-compilerTargetVM${javac.target}"/>
<argvalue="-javaEncoding${source.encoding}"/>
<classpathpath="${java.home}/../lib/tools.jar:${libs.jsp-compiler.classpath}:${libs.jsp-compilation.classpath}"/>
</java>
<mkdirdir="${build.generated.dir}/classes"/>
<webproject2:javacclasspath="${build.classes.dir}:${libs.jsp-compilation.classpath}:${javac.classpath}:${j2ee.platform.classpath}"destdir="${build.generated.dir}/classes"srcdir="${build.generated.dir}/src">
<customize>
<patternsetincludes="${javac.jsp.includes}"/>
</customize>
</webproject2:javac>
</target>
<targetname="compile-single-jsp">
<failunless="jsp.includes">MustselectafileintheIDEorsetjsp.includes</fail>
<antcalltarget="-do-compile-single-jsp"/>
</target>
<!--
DISTBUILDINGSECTION
-->
<targetname="-pre-dist">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,compile,compile-jsps,-pre-dist"if="do.war.package.without.custom.manifest"name="-do-dist-without-manifest">
<dirnamefile="${dist.war}"property="dist.jar.dir"/>
<mkdirdir="${dist.jar.dir}"/>
<jarcompress="${jar.compress}"jarfile="${dist.war}">
<filesetdir="${build.web.dir}"excludes="WEB-INF/classes/.netbeans_*,${dist.archive.excludes}"/>
</jar>
</target>
<targetdepends="init,compile,compile-jsps,-pre-dist"if="do.war.package.with.custom.manifest"name="-do-dist-with-manifest">
<dirnamefile="${dist.war}"property="dist.jar.dir"/>
<mkdirdir="${dist.jar.dir}"/>
<jarcompress="${jar.compress}"jarfile="${dist.war}"manifest="${build.meta.inf.dir}/MANIFEST.MF">
<filesetdir="${build.web.dir}"excludes="WEB-INF/classes/.netbeans_*,${dist.archive.excludes}"/>
</jar>
</target>
<targetdepends="init,compile,compile-jsps,-pre-dist"if="do.tmp.war.package.without.custom.manifest"name="-do-tmp-dist-without-manifest">
<dirnamefile="${dist.war}"property="dist.jar.dir"/>
<mkdirdir="${dist.jar.dir}"/>
<jarcompress="${jar.compress}"jarfile="${dist.war}">
<filesetdir="${build.web.dir}"excludes="WEB-INF/classes/.netbeans_*,${dist.archive.excludes}"/>
</jar>
</target>
<targetdepends="init,compile,compile-jsps,-pre-dist"if="do.tmp.war.package.with.custom.manifest"name="-do-tmp-dist-with-manifest">
<dirnamefile="${dist.war}"property="dist.jar.dir"/>
<mkdirdir="${dist.jar.dir}"/>
<jarcompress="${jar.compress}"jarfile="${dist.war}"manifest="${build.meta.inf.dir}/MANIFEST.MF">
<filesetdir="${build.web.dir}"excludes="WEB-INF/classes/.netbeans_*,${dist.archive.excludes}"/>
</jar>
</target>
<targetdepends="init,compile,compile-jsps,-pre-dist,-do-dist-with-manifest,-do-dist-without-manifest"name="do-dist"/>
<targetdepends="init"if="dist.ear.dir"name="library-inclusion-in-manifest">
<copyfilesfiles="${file.reference.jstl-1.2.jar}"iftldtodir="${build.web.dir}/WEB-INF"todir="${dist.ear.dir}/lib"/>
<copyfilesfiles="${file.reference.mysql-connector-java-5.1.5-bin.jar}"iftldtodir="${build.web.dir}/WEB-INF"todir="${dist.ear.dir}/lib"/>
<copyfilesfiles="${file.reference.taglibs-standard-impl-1.2.5.jar}"iftldtodir="${build.web.dir}/WEB-INF"todir="${dist.ear.dir}/lib"/>
<mkdirdir="${build.web.dir}/META-INF"/>
<manifestfile="${build.web.dir}/META-INF/MANIFEST.MF"mode="update"/>
</target>
<targetdepends="init"name="library-inclusion-in-archive"unless="dist.ear.dir">
<copyfilesfiles="${file.reference.jstl-1.2.jar}"todir="${build.web.dir}/WEB-INF/lib"/>
<copyfilesfiles="${file.reference.mysql-connector-java-5.1.5-bin.jar}"todir="${build.web.dir}/WEB-INF/lib"/>
<copyfilesfiles="${file.reference.taglibs-standard-impl-1.2.5.jar}"todir="${build.web.dir}/WEB-INF/lib"/>
</target>
<targetdepends="init"if="dist.ear.dir"name="-clean-webinf-lib">
<deletedir="${build.web.dir}/WEB-INF/lib"/>
</target>
<targetdepends="init,-clean-webinf-lib,compile,compile-jsps,-pre-dist,library-inclusion-in-manifest"if="do.tmp.war.package"name="do-ear-dist">
<dirnamefile="${dist.ear.war}"property="dist.jar.dir"/>
<mkdirdir="${dist.jar.dir}"/>
<jarcompress="${jar.compress}"jarfile="${dist.ear.war}"manifest="${build.web.dir}/META-INF/MANIFEST.MF">
<filesetdir="${build.web.dir}"excludes="WEB-INF/classes/.netbeans_*,${dist.archive.excludes}"/>
</jar>
</target>
<targetname="-post-dist">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,compile,-pre-dist,do-dist,-post-dist"description="Builddistribution(WAR)."name="dist"/>
<targetdepends="init,-clean-webinf-lib,-init-cos,compile,-pre-dist,do-ear-dist,-post-dist"description="Builddistribution(WAR)tobepackagedintoanEAR."name="dist-ear"/>
<!--
EXECUTIONSECTION
-->
<targetdepends="run-deploy,run-display-browser"description="Deploytoserverandshowinbrowser."name="run"/>
<targetname="-pre-run-deploy">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetname="-post-run-deploy">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetname="-pre-nbmodule-run-deploy">
<!--Emptyplaceholderforeasiercustomization.-->
<!--ThistargetcanbeoverridenbyNetBeansmodules.Don'toverrideitdirectly,use-pre-run-deploytaskinstead.-->
</target>
<targetname="-post-nbmodule-run-deploy">
<!--Emptyplaceholderforeasiercustomization.-->
<!--ThistargetcanbeoverridenbyNetBeansmodules.Don'toverrideitdirectly,use-post-run-deploytaskinstead.-->
</target>
<targetname="-run-deploy-am">
<!--TasktodeploytotheAccessManagerruntime.-->
</target>
<targetdepends="init,-init-cos,compile,compile-jsps,-do-compile-single-jsp,-pre-dist,-do-tmp-dist-with-manifest,-do-tmp-dist-without-manifest,-pre-run-deploy,-pre-nbmodule-run-deploy,-run-deploy-nb,-init-deploy-ant,-deploy-ant,-run-deploy-am,-post-nbmodule-run-deploy,-post-run-deploy,-do-update-breakpoints"name="run-deploy"/>
<targetif="netbeans.home"name="-run-deploy-nb">
<nbdeployclientUrlPart="${client.urlPart}"debugmode="false"forceRedeploy="${forceRedeploy}"/>
</target>
<targetname="-init-deploy-ant"unless="netbeans.home">
<propertyname="deploy.ant.archive"value="${dist.war}"/>
<propertyname="deploy.ant.docbase.dir"value="${web.docbase.dir}"/>
<propertyname="deploy.ant.resource.dir"value="${resource.dir}"/>
<propertyname="deploy.ant.enabled"value="true"/>
</target>
<targetdepends="dist,-run-undeploy-nb,-init-deploy-ant,-undeploy-ant"name="run-undeploy"/>
<targetif="netbeans.home"name="-run-undeploy-nb">
<failmessage="UndeployisnotsupportedfromwithintheIDE"/>
</target>
<targetdepends="init,-pre-dist,dist,-post-dist"name="verify">
<nbverifyfile="${dist.war}"/>
</target>
<targetdepends="run-deploy,-init-display-browser,-display-browser-nb-old,-display-browser-nb,-display-browser-cl"name="run-display-browser"/>
<targetif="do.display.browser"name="-init-display-browser">
<conditionproperty="do.display.browser.nb.old">
<and>
<issetproperty="netbeans.home"/>
<not>
<issetproperty="browser.context"/>
</not>
</and>
</condition>
<conditionproperty="do.display.browser.nb">
<and>
<issetproperty="netbeans.home"/>
<issetproperty="browser.context"/>
</and>
</condition>
<conditionproperty="do.display.browser.cl">
<issetproperty="deploy.ant.enabled"/>
</condition>
</target>
<targetif="do.display.browser.nb.old"name="-display-browser-nb-old">
<nbbrowseurl="${client.url}"/>
</target>
<targetif="do.display.browser.nb"name="-display-browser-nb">
<nbbrowsecontext="${browser.context}"url="${client.url}"urlPath="${client.urlPart}"/>
</target>
<targetif="do.display.browser.cl"name="-get-browser"unless="browser">
<conditionproperty="browser"value="rundll32">
<osfamily="windows"/>
</condition>
<conditionelse=""property="browser.args"value="url.dll,FileProtocolHandler">
<osfamily="windows"/>
</condition>
<conditionproperty="browser"value="/usr/bin/open">
<osfamily="mac"/>
</condition>
<propertyenvironment="env"/>
<conditionproperty="browser"value="${env.BROWSER}">
<issetproperty="env.BROWSER"/>
</condition>
<conditionproperty="browser"value="/usr/bin/firefox">
<availablefile="/usr/bin/firefox"/>
</condition>
<conditionproperty="browser"value="/usr/local/firefox/firefox">
<availablefile="/usr/local/firefox/firefox"/>
</condition>
<conditionproperty="browser"value="/usr/bin/mozilla">
<availablefile="/usr/bin/mozilla"/>
</condition>
<conditionproperty="browser"value="/usr/local/mozilla/mozilla">
<availablefile="/usr/local/mozilla/mozilla"/>
</condition>
<conditionproperty="browser"value="/usr/sfw/lib/firefox/firefox">
<availablefile="/usr/sfw/lib/firefox/firefox"/>
</condition>
<conditionproperty="browser"value="/opt/csw/bin/firefox">
<availablefile="/opt/csw/bin/firefox"/>
</condition>
<conditionproperty="browser"value="/usr/sfw/lib/mozilla/mozilla">
<availablefile="/usr/sfw/lib/mozilla/mozilla"/>
</condition>
<conditionproperty="browser"value="/opt/csw/bin/mozilla">
<availablefile="/opt/csw/bin/mozilla"/>
</condition>
</target>
<targetdepends="-get-browser"if="do.display.browser.cl"name="-display-browser-cl">
<failunless="browser">
Browsernotfound,cannotlaunchthedeployedapplication.TrytosettheBROWSERenvironmentvariable.
</fail>
<propertyname="browse.url"value="${deploy.ant.client.url}${client.urlPart}"/>
<echo>Launching${browse.url}</echo>
<execexecutable="${browser}"spawn="true">
<argline="${browser.args}${browse.url}"/>
</exec>
</target>
<targetdepends="init,-init-cos,compile-single"name="run-main">
<failunless="run.class">MustselectonefileintheIDEorsetrun.class</fail>
<webproject1:javaclassname="${run.class}"/>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single"name="run-test-with-main">
<failunless="run.class">MustselectonefileintheIDEorsetrun.class</fail>
<webproject1:javaclassname="${run.class}"classpath="${run.test.classpath}"/>
</target>
<targetdepends="init"if="netbeans.home"name="-do-update-breakpoints">
<webproject1:nbjpdaappreloaded/>
</target>
<!--
DEBUGGINGSECTION
-->
<targetdepends="init,-init-cos,compile,compile-jsps,-do-compile-single-jsp,-pre-dist,-do-tmp-dist-with-manifest,-do-tmp-dist-without-manifest"description="DebugprojectinIDE."if="netbeans.home"name="debug">
<nbstartserverdebugmode="true"/>
<antcalltarget="connect-debugger"/>
<nbdeployclientUrlPart="${client.urlPart}"debugmode="true"forceRedeploy="true"/>
<antcalltarget="debug-display-browser-old"/>
<antcalltarget="debug-display-browser"/>
<antcalltarget="connect-client-debugger"/>
</target>
<targetif="do.debug.server"name="connect-debugger"unless="is.debugged">
<conditionproperty="listeningcp"value="sourcepath">
<istruevalue="${j2ee.compile.on.save}"/>
</condition>
<nbjpdaconnectaddress="${jpda.address}"host="${jpda.host}"listeningcp="${listeningcp}"name="${name}"transport="${jpda.transport}">
<classpath>
<pathpath="${debug.classpath}:${j2ee.platform.classpath}"/>
</classpath>
<sourcepath>
<pathpath="${web.docbase.dir}"/>
</sourcepath>
</nbjpdaconnect>
</target>
<targetif="do.display.browser.debug.old"name="debug-display-browser-old">
<nbbrowseurl="${client.url}"/>
</target>
<targetif="do.display.browser.debug"name="debug-display-browser">
<nbbrowsecontext="${browser.context}"url="${client.url}"urlPath="${client.urlPart}"/>
</target>
<targetif="do.debug.client"name="connect-client-debugger">
<webproject1:nbjsdebugstartwebUrl="${client.url}"/>
</target>
<targetdepends="init,compile-test-single"if="netbeans.home"name="-debug-start-debuggee-main-test">
<failunless="debug.class">MustselectonefileintheIDEorsetdebug.class</fail>
<webproject1:debugclassname="${debug.class}"classpath="${debug.test.classpath}"/>
</target>
<targetdepends="init,compile-test-single,-debug-start-debugger-main-test,-debug-start-debuggee-main-test"if="netbeans.home"name="debug-test-with-main"/>
<targetdepends="init,compile,compile-jsps,-do-compile-single-jsp,debug"if="netbeans.home"name="debug-single"/>
<targetdepends="init"if="netbeans.home"name="-debug-start-debugger-main-test">
<webproject1:nbjpdastartclasspath="${debug.test.classpath}"name="${debug.class}"/>
</target>
<targetdepends="init"if="netbeans.home"name="-debug-start-debugger">
<webproject1:nbjpdastartname="${debug.class}"/>
</target>
<targetdepends="init,compile-single"if="netbeans.home"name="-debug-start-debuggee-single">
<failunless="debug.class">MustselectonefileintheIDEorsetdebug.class</fail>
<webproject1:debugclassname="${debug.class}"/>
</target>
<targetdepends="init,compile-single,-debug-start-debugger,-debug-start-debuggee-single"if="netbeans.home"name="debug-single-main"/>
<targetdepends="init"name="-pre-debug-fix">
<failunless="fix.includes">Mustsetfix.includes</fail>
<propertyname="javac.includes"value="${fix.includes}.java"/>
</target>
<targetdepends="init,-pre-debug-fix,compile-single"if="netbeans.home"name="-do-debug-fix">
<webproject1:nbjpdareload/>
</target>
<targetdepends="init,-pre-debug-fix,-do-debug-fix"if="netbeans.home"name="debug-fix"/>
<!--
=================
PROFILINGSECTION
=================
-->
<!--
preNB7.2profilingsection;consideritdeprecated
-->
<targetdescription="ProfileaJ2EEprojectintheIDE."if="profiler.info.jvmargs.agent"name="-profile-pre72">
<conditionelse="start-profiled-server"property="profiler.startserver.target"value="start-profiled-server-extraargs">
<issetproperty="profiler.info.jvmargs.extra"/>
</condition>
<antcalltarget="${profiler.startserver.target}"/>
<antcalltarget="run"/>
<antcalltarget="-profile-start-loadgen"/>
</target>
<targetif="profiler.info.jvmargs.agent"name="start-profiled-server">
<nbstartprofiledserverforceRestart="${profiler.j2ee.serverForceRestart}"javaPlatform="${profiler.info.javaPlatform}"startupTimeout="${profiler.j2ee.serverStartupTimeout}">
<jvmargvalue="${profiler.info.jvmargs.agent}"/>
<jvmargvalue="${profiler.j2ee.agentID}"/>
</nbstartprofiledserver>
</target>
<targetif="profiler.info.jvmargs.agent"name="start-profiled-server-extraargs">
<nbstartprofiledserverforceRestart="${profiler.j2ee.serverForceRestart}"javaPlatform="${profiler.info.javaPlatform}"startupTimeout="${profiler.j2ee.serverStartupTimeout}">
<jvmargvalue="${profiler.info.jvmargs.extra}"/>
<jvmargvalue="${profiler.info.jvmargs.agent}"/>
<jvmargvalue="${profiler.j2ee.agentID}"/>
</nbstartprofiledserver>
</target>
<targetdepends="profile-init,compile-test-single"if="profiler.info.jvmargs.agent"name="-profile-test-single-pre72">
<failunless="netbeans.home">ThistargetonlyworkswhenrunfrominsidetheNetBeansIDE.</fail>
<nbprofiledirect>
<classpath>
<pathpath="${run.test.classpath}"/>
<pathpath="${j2ee.platform.classpath}"/>
</classpath>
</nbprofiledirect>
<junitdir="${profiler.info.dir}"errorproperty="tests.failed"failureproperty="tests.failed"fork="true"jvm="${profiler.info.jvm}"showoutput="true">
<envkey="${profiler.info.pathvar}"path="${profiler.info.agentpath}:${profiler.current.path}"/>
<jvmargvalue="${profiler.info.jvmargs.agent}"/>
<jvmargline="${profiler.info.jvmargs}"/>
<testname="${profile.class}"/>
<classpath>
<pathpath="${run.test.classpath}"/>
<pathpath="${j2ee.platform.classpath}"/>
</classpath>
<syspropertyset>
<propertyrefprefix="test-sys-prop."/>
<mapperfrom="test-sys-prop.*"to="*"type="glob"/>
</syspropertyset>
<formattertype="brief"usefile="false"/>
<formattertype="xml"/>
</junit>
</target>
<targetif="netbeans.home"name="-profile-check">
<conditionproperty="profiler.configured">
<or>
<containscasesensitive="true"string="${run.jvmargs.ide}"substring="-agentpath:"/>
<containscasesensitive="true"string="${run.jvmargs.ide}"substring="-javaagent:"/>
</or>
</condition>
</target>
<targetdepends="init,-init-cos,compile,compile-jsps,-do-compile-single-jsp,-pre-dist,-do-tmp-dist-with-manifest,-do-tmp-dist-without-manifest"name="-do-profile">
<startprofiler/>
<nbstartserverprofilemode="true"/>
<nbdeployclientUrlPart="${client.urlPart}"forceRedeploy="true"profilemode="true"/>
<antcalltarget="debug-display-browser-old"/>
<antcalltarget="debug-display-browser"/>
<antcalltarget="-profile-start-loadgen"/>
</target>
<targetdepends="-profile-check,-profile-pre72"description="ProfileaJ2EEprojectintheIDE."if="profiler.configured"name="profile"unless="profiler.info.jvmargs.agent">
<antcalltarget="-do-profile"/>
</target>
<targetdepends="-profile-test-single-pre72"name="profile-test-single"/>
<targetdepends="-profile-check"if="profiler.configured"name="profile-test"unless="profiler.info.jvmargs.agent">
<startprofiler/>
<antcalltarget="test-single"/>
</target>
<targetif="profiler.loadgen.path"name="-profile-start-loadgen">
<loadgenstartpath="${profiler.loadgen.path}"/>
</target>
<!--
JAVADOCSECTION
-->
<targetdepends="init"if="have.sources"name="javadoc-build">
<mkdirdir="${dist.javadoc.dir}"/>
<javadocadditionalparam="${javadoc.additionalparam}"author="${javadoc.author}"charset="UTF-8"destdir="${dist.javadoc.dir}"docencoding="UTF-8"encoding="${javadoc.encoding.used}"failonerror="true"noindex="${javadoc.noindex}"nonavbar="${javadoc.nonavbar}"notree="${javadoc.notree}"private="${javadoc.private}"source="${javac.source}"splitindex="${javadoc.splitindex}"use="${javadoc.use}"useexternalfile="true"version="${javadoc.version}"windowtitle="${javadoc.windowtitle}">
<classpath>
<pathpath="${javac.classpath}:${j2ee.platform.classpath}"/>
</classpath>
<filesetdir="${src.dir}"excludes="${excludes}"includes="${includes}">
<filenamename="**/*.java"/>
</fileset>
<filesetdir="${build.generated.sources.dir}"erroronmissingdir="false">
<includename="**/*.java"/>
</fileset>
</javadoc>
<copytodir="${dist.javadoc.dir}">
<filesetdir="${src.dir}"excludes="${excludes}"includes="${includes}">
<filenamename="**/doc-files/**"/>
</fileset>
<filesetdir="${build.generated.sources.dir}"erroronmissingdir="false">
<includename="**/doc-files/**"/>
</fileset>
</copy>
</target>
<targetdepends="init,javadoc-build"if="netbeans.home"name="javadoc-browse"unless="no.javadoc.preview">
<nbbrowsefile="${dist.javadoc.dir}/index.html"/>
</target>
<targetdepends="init,javadoc-build,javadoc-browse"description="BuildJavadoc."name="javadoc"/>
<!--

TESTCOMPILATIONSECTION
-->
<targetdepends="init,compile"if="have.tests"name="-pre-pre-compile-test">
<mkdirdir="${build.test.classes.dir}"/>
<propertyname="j2ee.platform.embeddableejb.classpath"value=""/>
</target>
<targetname="-pre-compile-test">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,compile,-pre-pre-compile-test,-pre-compile-test"if="have.tests"name="-do-compile-test">
<webproject2:javacclasspath="${javac.test.classpath}:${j2ee.platform.classpath}:${j2ee.platform.embeddableejb.classpath}"debug="true"destdir="${build.test.classes.dir}"srcdir="${test.src.dir}"/>
<copytodir="${build.test.classes.dir}">
<filesetdir="${test.src.dir}"excludes="${build.classes.excludes},${excludes}"includes="${includes}"/>
</copy>
</target>
<targetname="-post-compile-test">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,compile,-pre-pre-compile-test,-pre-compile-test,-do-compile-test,-post-compile-test"name="compile-test"/>
<targetname="-pre-compile-test-single">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,compile,-pre-pre-compile-test,-pre-compile-test-single"if="have.tests"name="-do-compile-test-single">
<failunless="javac.includes">MustselectsomefilesintheIDEorsetjavac.includes</fail>
<webproject2:javacclasspath="${javac.test.classpath}:${j2ee.platform.classpath}:${j2ee.platform.embeddableejb.classpath}"debug="true"destdir="${build.test.classes.dir}"excludes=""includes="${javac.includes}"srcdir="${test.src.dir}"/>
<copytodir="${build.test.classes.dir}">
<filesetdir="${test.src.dir}"excludes="${build.classes.excludes},${excludes}"includes="${includes}"/>
</copy>
</target>
<targetname="-post-compile-test-single">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,compile,-pre-pre-compile-test,-pre-compile-test-single,-do-compile-test-single,-post-compile-test-single"name="compile-test-single"/>
<!--

TESTEXECUTIONSECTION
-->
<targetdepends="init"if="have.tests"name="-pre-test-run">
<mkdirdir="${build.test.results.dir}"/>
</target>
<targetdepends="init,compile-test,-pre-test-run"if="have.tests"name="-do-test-run">
<webproject2:testincludes="${includes}"testincludes="**/*Test.java"/>
</target>
<targetdepends="init,compile-test,-pre-test-run,-do-test-run"if="have.tests"name="-post-test-run">
<failif="tests.failed"unless="ignore.failing.tests">Sometestsfailed;seedetailsabove.</fail>
</target>
<targetdepends="init"if="have.tests"name="test-report"/>
<targetdepends="init"if="netbeans.home+have.tests"name="-test-browse"/>
<targetdepends="init,compile-test,-pre-test-run,-do-test-run,test-report,-post-test-run,-test-browse"description="Rununittests."name="test"/>
<targetdepends="init"if="have.tests"name="-pre-test-run-single">
<mkdirdir="${build.test.results.dir}"/>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single"if="have.tests"name="-do-test-run-single">
<failunless="test.includes">MustselectsomefilesintheIDEorsettest.includes</fail>
<webproject2:testexcludes=""includes="${test.includes}"testincludes="${test.includes}"/>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single,-do-test-run-single"if="have.tests"name="-post-test-run-single">
<failif="tests.failed"unless="ignore.failing.tests">Sometestsfailed;seedetailsabove.</fail>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single,-do-test-run-single,-post-test-run-single"description="Runsingleunittest."name="test-single"/>
<targetdepends="init,compile-test-single,-pre-test-run-single"if="have.tests"name="-do-test-run-single-method">
<failunless="test.class">MustselectsomefilesintheIDEorsettest.class</fail>
<failunless="test.method">MustselectsomemethodintheIDEorsettest.method</fail>
<webproject2:testexcludes=""includes="${javac.includes}"testincludes="${test.class}"testmethods="${test.method}"/>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single,-do-test-run-single-method"if="have.tests"name="-post-test-run-single-method">
<failif="tests.failed"unless="ignore.failing.tests">Sometestsfailed;seedetailsabove.</fail>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single,-do-test-run-single-method,-post-test-run-single-method"description="Runsingleunittest."name="test-single-method"/>
<!--

TESTDEBUGGINGSECTION
-->
<targetdepends="init,compile-test-single,-pre-test-run-single"if="have.tests"name="-debug-start-debuggee-test">
<failunless="test.class">MustselectonefileintheIDEorsettest.class</fail>
<webproject2:test-debugexcludes=""includes="${javac.includes}"testClass="${test.class}"testincludes="${javac.includes}"/>
</target>
<targetdepends="init,compile-test-single,-pre-test-run-single"if="have.tests"name="-debug-start-debuggee-test-method">
<failunless="test.class">MustselectonefileintheIDEorsettest.class</fail>
<failunless="test.method">MustselectsomemethodintheIDEorsettest.method</fail>
<webproject2:test-debugexcludes=""includes="${javac.includes}"testClass="${test.class}"testMethod="${test.method}"testincludes="${test.class}"testmethods="${test.method}"/>
</target>
<targetdepends="init,compile-test"if="netbeans.home+have.tests"name="-debug-start-debugger-test">
<webproject1:nbjpdastartclasspath="${debug.test.classpath}"name="${test.class}"/>
</target>
<targetdepends="init,compile-test,-debug-start-debugger-test,-debug-start-debuggee-test"name="debug-test"/>
<targetdepends="init,compile-test-single,-debug-start-debugger-test,-debug-start-debuggee-test-method"name="debug-test-method"/>
<targetdepends="init,-pre-debug-fix,compile-test-single"if="netbeans.home"name="-do-debug-fix-test">
<webproject1:nbjpdareloaddir="${build.test.classes.dir}"/>
</target>
<targetdepends="init,-pre-debug-fix,-do-debug-fix-test"if="netbeans.home"name="debug-fix-test"/>
<!--

CLEANUPSECTION
-->
<targetdepends="init"name="deps-clean"unless="no.deps"/>
<targetdepends="init"name="do-clean">
<conditionproperty="build.dir.to.clean"value="${build.web.dir}">
<issetproperty="dist.ear.dir"/>
</condition>
<propertyname="build.dir.to.clean"value="${build.web.dir}"/>
<deleteincludeEmptyDirs="true"quiet="true">
<filesetdir="${build.dir.to.clean}/WEB-INF/lib"/>
</delete>
<deletedir="${build.dir}"/>
<availablefile="${build.dir.to.clean}/WEB-INF/lib"property="status.clean-failed"type="dir"/>
<deletedir="${dist.dir}"/>
</target>
<targetdepends="do-clean"if="status.clean-failed"name="check-clean">
<echomessage="Warning:unabletodeletesomefilesin${build.web.dir}/WEB-INF/lib-theyareprobablylockedbytheJ2EEserver."/>
<echolevel="info"message="TodeleteallfilesundeploythemodulefromServerRegistryinRuntimetabandthenuseCleanagain."/>
</target>
<targetdepends="init"if="netbeans.home"name="undeploy-clean">
<nbundeployfailOnError="false"startServer="false"/>
</target>
<targetname="-post-clean">
<!--Emptyplaceholderforeasiercustomization.-->
<!--Youcanoverridethistargetinthe../build.xmlfile.-->
</target>
<targetdepends="init,undeploy-clean,deps-clean,do-clean,check-clean,-post-clean"description="Cleanbuildproducts."name="clean"/>
<targetdepends="clean"description="Cleanbuildproducts."name="clean-ear"/>
</project>
```

#### ant-deploy.xml
- ant-deploy.xml
  - Description: Code from programlisting
  - Source Code:
```java
<?xmlversion="1.0"encoding="UTF-8"?>
<!--
DONOTALTERORREMOVECOPYRIGHTNOTICESORTHISHEADER.

Copyright(c)2006,2016Oracleand/oritsaffiliates.Allrightsreserved.

OracleandJavaareregisteredtrademarksofOracleand/oritsaffiliates.
Othernamesmaybetrademarksoftheirrespectiveowners.

ThecontentsofthisfilearesubjecttothetermsofeithertheGNU
GeneralPublicLicenseVersion2only("GPL")ortheCommon
DevelopmentandDistributionLicense("CDDL")(collectively,the
"License").Youmaynotusethisfileexceptincompliancewiththe
License.YoucanobtainacopyoftheLicenseat
http://www.netbeans.org/cddl-gplv2.html
ornbbuild/licenses/CDDL-GPL-2-CP.SeetheLicenseforthe
specificlanguagegoverningpermissionsandlimitationsunderthe
License.Whendistributingthesoftware,includethisLicenseHeader
NoticeineachfileandincludetheLicensefileat
nbbuild/licenses/CDDL-GPL-2-CP.Oracledesignatesthis
particularfileassubjecttothe"Classpath"exceptionasprovided
byOracleintheGPLVersion2sectionoftheLicensefilethat
accompaniedthiscode.Ifapplicable,addthefollowingbelowthe
LicenseHeader,withthefieldsenclosedbybrackets[]replacedby
yourownidentifyinginformation:
"PortionsCopyrighted[year][nameofcopyrightowner]"

IfyouwishyourversionofthisfiletobegovernedbyonlytheCDDL
oronlytheGPLVersion2,indicateyourdecisionbyadding
"[Contributor]electstoincludethissoftwareinthisdistribution
underthe[CDDLorGPLVersion2]license."Ifyoudonotindicatea
singlechoiceoflicense,arecipienthastheoptiontodistribute
yourversionofthisfileundereithertheCDDL,theGPLVersion2or
toextendthechoiceoflicensetoitslicenseesasprovidedabove.
However,ifyouaddGPLVersion2codeandtherefore,electedtheGPL
Version2license,thentheoptionappliesonlyifthenewcodeis
madesubjecttosuchoptionbythecopyrightholder.

Contributor(s):
-->
<projectdefault="-deploy-ant"basedir=".">
<targetname="-init"if="deploy.ant.enabled">
<propertyfile="${deploy.ant.properties.file}"/>
<tempfileproperty="temp.module.folder"prefix="tomcat"destdir="${java.io.tmpdir}"/>
<unwarsrc="${deploy.ant.archive}"dest="${temp.module.folder}">
<patternsetincludes="META-INF/context.xml"/>
</unwar>
<xmlpropertyfile="${temp.module.folder}/META-INF/context.xml"/>
<deletedir="${temp.module.folder}"/>
</target>
<targetname="-check-credentials"if="deploy.ant.enabled"depends="-init">
<failmessage="Tomcatpasswordhastobepassedastomcat.passwordproperty.">
<condition>
<not>
<issetproperty="tomcat.password"/>
</not>
</condition>
</fail>
</target>
<targetname="-deploy-ant"if="deploy.ant.enabled"depends="-init,-check-credentials">
<echomessage="Deploying${deploy.ant.archive}to${Context(path)}"/>
<taskdefname="deploy"classname="org.apache.catalina.ant.DeployTask"
classpath="${tomcat.home}/server/lib/catalina-ant.jar"/>
<deployurl="${tomcat.url}/manager"username="${tomcat.username}"
password="${tomcat.password}"path="${Context(path)}"
war="${deploy.ant.archive}"/>
<propertyname="deploy.ant.client.url"value="${tomcat.url}${Context(path)}"/>
</target>
<targetname="-undeploy-ant"if="deploy.ant.enabled"depends="-init,-check-credentials">
<echomessage="Undeploying${Context(path)}"/>
<taskdefname="undeploy"classname="org.apache.catalina.ant.UndeployTask"
classpath="${tomcat.home}/server/lib/catalina-ant.jar"/>
<undeployurl="${tomcat.url}/manager"username="${tomcat.username}"
password="${tomcat.password}"path="${Context(path)}"/>
</target>
</project>
```

#### build.xml
- build.xml
  - Description: Code from programlisting
  - Source Code:
```java
<?xmlversion="1.0"encoding="UTF-8"?>
<!--Youmayfreelyeditthisfile.Seecommentedblocksbelowfor-->
<!--someexamplesofhowtocustomizethebuild.-->
<!--(Ifyoudeleteitandreopentheprojectitwillberecreated.)-->
<!--Bydefault,onlytheCleanandBuildcommandsusethisbuildscript.-->
<!--CommandssuchasRun,Debug,andTestonlyusethisbuildscriptif-->
<!--theCompileonSavefeatureisturnedofffortheproject.-->
<!--YoucanturnofftheCompileonSave(orDeployonSave)setting-->
<!--intheproject'sProjectPropertiesdialogbox.-->
<projectname="HospitalManagementSystem"default="default"basedir=".">
<description>Builds,tests,andrunstheprojectHospitalManagementSystem.</description>
<importfile="nbproject/build-impl.xml"/>
<!--

Thereexistseveraltargetswhicharebydefaultemptyandwhichcanbe
usedforexecutionofyourtasks.Thesetargetsareusuallyexecuted
beforeandaftersomemaintargets.Theyare:

-pre-init:calledbeforeinitializationofprojectproperties
-post-init:calledafterinitializationofprojectproperties
-pre-compile:calledbeforejavaccompilation
-post-compile:calledafterjavaccompilation
-pre-compile-single:calledbeforejavaccompilationofsinglefile
-post-compile-single:calledafterjavaccompilationofsinglefile
-pre-compile-test:calledbeforejavaccompilationofJUnittests
-post-compile-test:calledafterjavaccompilationofJUnittests
-pre-compile-test-single:calledbeforejavaccompilationofsingleJUnittest
-post-compile-test-single:calledafterjavaccompilationofsingleJUunittest
-pre-dist:calledbeforearchivebuilding
-post-dist:calledafterarchivebuilding
-post-clean:calledaftercleaningbuildproducts
-pre-run-deploy:calledbeforedeploying
-post-run-deploy:calledafterdeploying

Exampleofpluginganobfuscatorafterthecompilationcouldlooklike

<targetname="-post-compile">
<obfuscate>
<filesetdir="${build.classes.dir}"/>
</obfuscate>
</target>

Forlistofavailablepropertieschecktheimported
nbproject/build-impl.xmlfile.


Otherwayhowtocustomizethebuildisbyoverridingexistingmaintargets.
Thetargetofinterestare:

init-macrodef-javac:definesmacroforjavaccompilation
init-macrodef-junit:definesmacroforjunitexecution
init-macrodef-debug:definesmacroforclassdebugging
do-dist:archivebuilding
run:executionofproject
javadoc-build:javadocgeneration

Exampleofoverridingthetargetforprojectexecutioncouldlooklike

<targetname="run"depends="<PROJNAME>-impl.jar">
<execdir="bin"executable="launcher.exe">
<argfile="${dist.jar}"/>
</exec>
</target>

Noticethatoverriddentargetdependsonjartargetandnotonlyon
compiletargetasregularruntargetdoes.Again,forlistofavailable
propertieswhichyoucanusecheckthetargetyouareoverridingin
nbproject/build-impl.xmlfile.

-->
</project>
```

### Cluster 8
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### adminLogin.jsp
- adminLogin.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<!DOCTYPEhtml>
<html>
<head>
<metacharset="ISO-8859-1">
<title>HospitalManagementSystem</title>
<linkrel="stylesheet"href="fonts/material-icon/css/material-design-iconic-font.min.css">
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"href="css/register.css"type="text/css"/>
</head>
<styletype="text/css">
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}

.img-rounded{
height:100%;
width:100%;
}

h1{
color:white;
text-align:center;
}
</style>
<body>
<navclass="navbarnavbar-expand-mdnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttontype="button"class="navbar-toggler"data-toggle="collapse"
data-target="#navbarCollapse">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarCollapse">
<divclass="navbar-navml-auto"style="margin-right:30px;">
<aclass="dropdown-item"href="index.jsp">Home</a>
<aclass="dropdown-item"href="adminLogin.jsp">Admin</a>
</div>
</div>
</nav>
<div>
<h1>
<b>HospitalManagementSystem</b>
</h1>
</div>
<!--SinginForm-->
<formaction="<%=request.getContextPath()%>/AdminLogin"method="post">
<sectionclass="sign-in">
<divclass="container">
<divclass="signin-content">
<divclass="signin-image">
<figure><imgsrc="img/signin-image.jpg"alt="singupimage"></figure>
<ahref="adminRegister.jsp"class="signup-image-link">Createanaccount</a>
</div>

<divclass="signin-form">
<h2class="form-title">Signin</h2>
<formmethod="POST"class="register-form"id="login-form">
<divclass="form-group">
<labelfor="your_name"><iclass="zmdizmdi-accountmaterial-icons-name"></i></label>
<inputtype="text"name="your_name"id="your_name"placeholder="UserName"/>
</div>
<divclass="form-group">
<labelfor="your_pass"><iclass="zmdizmdi-lock"></i></label>
<inputtype="password"name="your_pass"id="your_pass"placeholder="Password"/>
</div>
<divclass="form-group">
<inputtype="checkbox"name="remember-me"id="remember-me"class="agree-term"/>
<labelfor="remember-me"class="label-agree-term"><span><span></span></span>Rememberme</label>
</div>
<divclass="form-groupform-button">
<inputtype="submit"name="signin"id="signin"class="form-submit"value="Login"/>
</div>
</form>
</div>
</div>
</div>
</section>
</form>
</body>
</html>
```

#### adminRegister.jsp
- adminRegister.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<!DOCTYPEhtml>
<html>
<head>
<metacharset="ISO-8859-1">
<title>HospitalManagementSystem</title>
<linkrel="stylesheet"href="fonts/material-icon/css/material-design-iconic-font.min.css">
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"href="css/register.css"type="text/css"/>
</head>
<styletype="text/css">
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}

.img-rounded{
height:100%;
width:100%;
}

h1{
color:white;
text-align:center;
}
</style>
<body>
<navclass="navbarnavbar-expand-mdnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttontype="button"class="navbar-toggler"data-toggle="collapse"
data-target="#navbarCollapse">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarCollapse">
<divclass="navbar-navml-auto"style="margin-right:30px;">
<aclass="dropdown-item"href="index.jsp">Home</a>
<aclass="dropdown-item"href="adminLogin.jsp">Admin</a>
</div>
</div>
</nav>
<div>
<h1>
<b>HospitalManagementSystem</b>
</h1>
</div>
<formaction="<%=request.getContextPath()%>/AdminRegister"method="post">
<!--Signupform-->
<sectionclass="signup">
<divclass="container">
<divclass="signup-content">
<divclass="signup-form">
<h2class="form-title">Signup</h2>
<formmethod="POST"class="register-form"id="register-form">
<divclass="form-group">
<labelfor="email"><iclass="zmdizmdi-email"></i></label>
<inputtype="email"name="email"id="email"placeholder="YourEmail"/>
</div>
<divclass="form-group">
<labelfor="pass"><iclass="zmdizmdi-lock"></i></label>
<inputtype="password"name="pass"id="pass"placeholder="Password"/>
</div>
<divclass="form-group">
<labelfor="re-pass"><iclass="zmdizmdi-lock-outline"></i></label>
<inputtype="password"name="re_pass"id="re_pass"placeholder="Repeatyourpassword"/>
</div>
<divclass="form-group">
<inputtype="checkbox"name="agree-term"id="agree-term"class="agree-term"/>
<labelfor="agree-term"class="label-agree-term"><span><span></span></span>Iagreeallstatementsin<ahref="#"class="term-service">Termsofservice</a></label>
</div>
<divclass="form-groupform-button">
<inputtype="submit"name="signup"id="signup"class="form-submit"value="Register"/>
</div>
</form>
</div>
<divclass="signup-image">
<figure><imgsrc="img/signup-image.jpg"alt="singupimage"></figure>
<ahref="adminLogin.jsp"class="signup-image-link">Iamalreadymember</a>
</div>
</div>
</div>
</section>
</form>
</body>
</html>
```

### Cluster 6
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### updatePatient.jsp
- updatePatient.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:updatePatient
Createdon:19Aug,2020,5:19:02PM
Author:Admin
--%>

<%pageimport="java.sql.Statement"%>
<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.PreparedStatement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pageimport="java.sql.Connection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>UpdatePatient</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
</style>
</head>
<body>

<%
Stringmob=request.getParameter("mob");
Connectioncon=DatabaseConnection.initializeDatabase();
Strings="SELECT*FROMpatientWHEREmobile='"+mob+"'";
PreparedStatementpstmt=con.prepareStatement(s);
ResultSetrs=pstmt.executeQuery();
while(rs.next()){
%>
<divclass="container-contact100">


<divclass="wrap-contact100">
<divclass="contact100-form-title"style="background-image:url(img/bg-01.jpg);">
<spanclass="contact100-form-title-1">
PatientRegistrationForm
</span>
</div>

<formclass="contact100-formvalidate-form"action="<%=request.getContextPath()%>/updatePatient"method="post">
<divclass="wrap-input100validate-input"data-validate="FirstNameisrequired">
<spanclass="label-input100">First_Name:</span>
<inputclass="input100"type="text"value="<%=rs.getString(1)%>"name="fname"placeholder="EnterFirstname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="LastNameisrequired">
<spanclass="label-input100">Last_Name:</span>
<inputclass="input100"type="text"value="<%=rs.getString(2)%>"name="lname"placeholder="EnterLastname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="genderisrequired">
<spanclass="label-input100">Gender:</span>
<inputclass="input100"type="text"value="<%=rs.getString(3)%>"name="gender"placeholder="EnterGender">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Phoneisrequired">
<spanclass="label-input100">Phone:</span>
<inputclass="input100"type="text"value="<%=rs.getString(9)%>"name="Mobile"placeholder="Enterphonenumber">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Cityisrequired">
<spanclass="label-input100">City:</span>
<inputclass="input100"type="text"value="<%=rs.getString(4)%>"name="City"placeholder="EnterCity">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Validemailisrequired:exabc.xyz">
<spanclass="label-input100">Email:</span>
<inputclass="input100"type="text"value="<%=rs.getString(5)%>"name="email"placeholder="Enteremail">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Ageisrequired">
<spanclass="label-input100">Age:</span>
<inputclass="input100"type="text"value="<%=rs.getString(6)%>"name="age"placeholder="EnterAge">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Addressisrequired">
<spanclass="label-input100">Address</span>
<inputclass="input100"type="text"value="<%=rs.getString(7)%>"name="address"placeholder="EnterAddress">
<spanclass="focus-input100"></span>
</div>

<divclass="container-contact100-form-btn">
<buttonclass="contact100-form-btn">
<span>
Submit
<iclass="fafa-long-arrow-rightm-l-7"aria-hidden="true"></i>
</span>
</button>
</div>
</form>
</div>
</div>
<%
}
%>
</body>
</html>
```

#### index.jsp
- index.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<!DOCTYPEhtml>
<html>
<head>
<metacharset="ISO-8859-1">
<title>HospitalManagementSystem</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"href="css/style.css"type="text/css"/>
</head>
<styletype="text/css">
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}

.img-rounded{
height:100%;
width:100%;
}

h1{
color:white;
text-align:center;
}
</style>
<body>
<navclass="navbarnavbar-expand-mdnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttontype="button"class="navbar-toggler"data-toggle="collapse"
data-target="#navbarCollapse">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarCollapse">
<divclass="navbar-navml-auto"style="margin-right:30px;">
<aclass="dropdown-item"href="index.jsp">Home</a>
<aclass="dropdown-item"href="adminLogin.jsp">Admin</a>
</div>
</div>
</nav>
<div>
<h1>
<b>HospitalManagementSystem</b>
</h1>
</div>
<divclass="wrapperfadeInDown">
<divid="formContent">
<!--TabsTitles-->
<h2>UserLogin</h2>
<!--Icon-->
<divclass="fadeInfirst">

</div>

<!--LoginForm-->
<formaction="<%=request.getContextPath()%>/UserLogin"method="post">
<inputtype="text"id="Username"class="fadeInsecond"name="username"
placeholder="Username">
<inputtype="password"id="password"
class="fadeInthird"name="password"placeholder="password">
<input
type="submit"class="fadeInfourth"value="LogIn">
</form>

<!--RemindPassowrd-->
<divid="formFooter">
<aclass="underlineHover"href="userRegister.jsp">CreateAccount</a>
</div>

</div>
</div>
</body>
</html>
```

#### UserHome.jsp
- UserHome.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:13Aug,2020,9:56:36AM
Author:Admin
--%>

<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>UserHome</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<ulclass="navbar-navmr-auto">
<liclass="nav-itemactive">
<aclass="nav-link"href="index.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="listPatient.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
Billing
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="#">AddBill</a>
<aclass="dropdown-item"href="#">ViewBill</a>
</div>
</li>
</ul>
</div>
</nav>
</body>
</html>
```

#### userRegister.jsp
- userRegister.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<!DOCTYPEhtml>
<html>
<head>
<metacharset="ISO-8859-1">
<title>HospitalManagementSystem</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"href="css/style.css"type="text/css"/>
</head>
<styletype="text/css">
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}

.img-rounded{
height:100%;
width:100%;
}

h1{
color:white;
text-align:center;
}
</style>
<body>
<navclass="navbarnavbar-expand-mdnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttontype="button"class="navbar-toggler"data-toggle="collapse"
data-target="#navbarCollapse">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarCollapse">
<divclass="navbar-navml-auto"style="margin-right:30px;">
<aclass="dropdown-item"href="index.jsp">Home</a>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href=""id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
Admin
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="adminRegister.jsp">Register</a>
<aclass="dropdown-item"href="adminLogin.jsp">Login</a>
</div>
</li>
<liclass="nav-itemdropdown">

</li>
</div>
</div>
</nav>
<div>
<h1>
<b>HospitalManagementSystem</b>
</h1>
</div>
<divclass="wrapperfadeInDown">
<divid="formContent">
<!--TabsTitles-->
<h2>UserLogin</h2>
<!--Icon-->
<divclass="fadeInfirst">

</div>

<!--LoginForm-->
<formaction="<%=request.getContextPath()%>/UserRegister"method="post">
<inputtype="text"id="Username"class="fadeInsecond"name="Username"
placeholder="EnterUsername">
<inputtype="password"id="password"
class="fadeInthird"name="password"placeholder="EnterPassword">
<inputtype="password"id="password"
class="fadeInthird"name="repassword"placeholder="EnterPasswordAgain">
<input
type="submit"class="fadeInfourth"value="LogIn">
</form>

<!--RemindPassowrd-->
<divid="formFooter">
<aclass="underlineHover"href="index.jsp">Login</a>
</div>

</div>
</div>
</body>
</html>
```

### Cluster 2
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### AddDoctor.java
- AddDoctor.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjava.sql.SQLException;
importjava.text.DateFormat;
importjava.text.SimpleDateFormat;
importjava.util.Date;
importjava.util.logging.Level;
importjava.util.logging.Logger;
importjavax.servlet.RequestDispatcher;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/AddDoctor")
publicclassAddDoctorextendsHttpServlet{

privateinti;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
DatetodaysDate=newDate();
DateFormatdf2=newSimpleDateFormat("dd-MM-yyyyHH:mm:ss");

Stringsid=request.getParameter("id");
intid=Integer.parseInt(sid);
Stringfname=request.getParameter("fname");
Stringlname=request.getParameter("lname");
Stringgender=request.getParameter("gender");
Stringphone=request.getParameter("Mobile");
Stringcity=request.getParameter("City");
Stringemail=request.getParameter("email");
Stringage=request.getParameter("age");
Stringaddress=request.getParameter("address");
Stringqualification=request.getParameter("qualification");

StringDateAndTime=df2.format(todaysDate);

Connectioncon=DatabaseConnection.initializeDatabase();
PreparedStatementpst=con.prepareStatement("insertintodoctorvalues(?,?,?,?,?,?,?,?,?,?,?)");
pst.setInt(1,id);
pst.setString(5,phone);
pst.setString(2,fname);
pst.setString(3,lname);
pst.setString(4,gender);
pst.setString(6,city);
pst.setString(7,email);
pst.setString(8,age);
pst.setString(9,address);
pst.setString(10,DateAndTime);
pst.setString(11,qualification);

i=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('DataAddSuccessfully..!');");
pw.println("window.location.href=\"AdminHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AdminHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('Failed!!!!,tryAgainLater!');");
pw.println("window.location.href=\"addDoctor.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("addDoctor.jsp");
//rd.forward(request,response);
}
}catch(SQLException|ClassNotFoundExceptionex){
Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE,null,ex);
}
}

}
```

#### Controller::AddDoctor
- i
  - Description: i
  - Definition: int Controller.AddDoctor.i
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddDoctor.java
  - Source Code:
```java
    private int i;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String sid = request.getParameter("id");
            int id = Integer.parseInt(sid);
            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String gender = request.getParameter("gender");
            String phone = request.getParameter("Mobile");
            String city = request.getParameter("City");
            String email = request.getParameter("email");
            String age = request.getParameter("age");
            String address = request.getParameter("address");
            String qualification = request.getParameter("qualification");

            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into doctor values(?,?,?,?,?,?,?,?,?,?,?)");
            pst.setInt(1, id);
            pst.setString(5, phone);
            pst.setString(2, fname);
            pst.setString(3, lname);
            pst.setString(4, gender);
            pst.setString(6, city);
            pst.setString(7, email);
            pst.setString(8, age);
            pst.setString(9, address);
            pst.setString(10, DateAndTime);
            pst.setString(11, qualification);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Data Add Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Failed !!!!,try Again Later!');");
                pw.println("window.location.href = \"addDoctor.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("addDoctor.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.AddDoctor.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddDoctor.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String sid = request.getParameter("id");
            int id = Integer.parseInt(sid);
            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String gender = request.getParameter("gender");
            String phone = request.getParameter("Mobile");
            String city = request.getParameter("City");
            String email = request.getParameter("email");
            String age = request.getParameter("age");
            String address = request.getParameter("address");
            String qualification = request.getParameter("qualification");

            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into doctor values(?,?,?,?,?,?,?,?,?,?,?)");
            pst.setInt(1, id);
            pst.setString(5, phone);
            pst.setString(2, fname);
            pst.setString(3, lname);
            pst.setString(4, gender);
            pst.setString(6, city);
            pst.setString(7, email);
            pst.setString(8, age);
            pst.setString(9, address);
            pst.setString(10, DateAndTime);
            pst.setString(11, qualification);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Data Add Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Failed !!!!,try Again Later!');");
                pw.println("window.location.href = \"addDoctor.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("addDoctor.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
```

#### Controller::AddPatient
- i
  - Description: i
  - Definition: int Controller.AddPatient.i
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddPatient.java
  - Source Code:
```java
    private int i;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String gender = request.getParameter("gender");
            String phone = request.getParameter("Mobile");
            String city = request.getParameter("City");
            String email = request.getParameter("email");
            String age = request.getParameter("age");
            String address = request.getParameter("address");

            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into patient values(?,?,?,?,?,?,?,?,?)");
            pst.setString(9, phone);
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, gender);
            pst.setString(4, city);
            pst.setString(5, email);
            pst.setString(6, age);
            pst.setString(7, address);
            pst.setString(8, DateAndTime);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"UserHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("UserHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Incorrect Data..!');");
                pw.println("window.location.href = \"addpatient.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("addpatient.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.AddPatient.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddPatient.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String gender = request.getParameter("gender");
            String phone = request.getParameter("Mobile");
            String city = request.getParameter("City");
            String email = request.getParameter("email");
            String age = request.getParameter("age");
            String address = request.getParameter("address");

            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into patient values(?,?,?,?,?,?,?,?,?)");
            pst.setString(9, phone);
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, gender);
            pst.setString(4, city);
            pst.setString(5, email);
            pst.setString(6, age);
            pst.setString(7, address);
            pst.setString(8, DateAndTime);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"UserHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("UserHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Incorrect Data..!');");
                pw.println("window.location.href = \"addpatient.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("addpatient.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }

    }
```

#### updatePatient.java
- updatePatient.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/updatePatient")
publicclassupdatePatientextendsHttpServlet{

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();

Stringfname=request.getParameter("fname");
Stringlname=request.getParameter("lname");
Stringgender=request.getParameter("gender");
Stringphone=request.getParameter("Mobile");
Stringcity=request.getParameter("City");
Stringemail=request.getParameter("email");
Stringage=request.getParameter("age");
Stringaddress=request.getParameter("address");

try{
Connectioncon=DatabaseConnection.initializeDatabase();
PreparedStatementpst=con.prepareStatement("updatepatientsetfname=?,lname=?,gender=?,city=?,email=?,age=?,address=?wheremobile='"+phone+"'");
pst.setString(1,fname);
pst.setString(2,lname);
pst.setString(3,gender);
pst.setString(4,city);
pst.setString(5,email);
pst.setString(6,age);
pst.setString(7,address);

inti=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('UpdateSuccessfully..!');");
pw.println("window.location.href=\"AdminHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AdminHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('Failed..!TryAgainLater...');");
pw.println("window.location.href=\"updatePatient.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("updatePatient.jsp");
//rd.forward(request,response);
}
con.close();
}catch(Exceptione){

}

}
}
```

#### Controller::AddRecp
- i
  - Description: i
  - Definition: int Controller.AddRecp.i
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddRecp.java
  - Source Code:
```java
    private int i;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String phone = request.getParameter("Mobile");
            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into recp values(?,?,?,?)");
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, phone);
            pst.setString(4, DateAndTime);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Add Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Incorrect Data...!');");
                pw.println("window.location.href = \"AddRecp.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AddRecp.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.AddRecp.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddRecp.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String phone = request.getParameter("Mobile");
            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into recp values(?,?,?,?)");
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, phone);
            pst.setString(4, DateAndTime);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Add Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Incorrect Data...!');");
                pw.println("window.location.href = \"AddRecp.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AddRecp.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
```

#### AddPatient.java
- AddPatient.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjava.sql.SQLException;
importjava.text.DateFormat;
importjava.text.SimpleDateFormat;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;
importjava.util.Date;
importjava.util.logging.Level;
importjava.util.logging.Logger;
importjavax.servlet.RequestDispatcher;

WebServlet("/AddPatient")
publicclassAddPatientextendsHttpServlet{

privateinti;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
DatetodaysDate=newDate();
DateFormatdf2=newSimpleDateFormat("dd-MM-yyyyHH:mm:ss");

Stringfname=request.getParameter("fname");
Stringlname=request.getParameter("lname");
Stringgender=request.getParameter("gender");
Stringphone=request.getParameter("Mobile");
Stringcity=request.getParameter("City");
Stringemail=request.getParameter("email");
Stringage=request.getParameter("age");
Stringaddress=request.getParameter("address");

StringDateAndTime=df2.format(todaysDate);

Connectioncon=DatabaseConnection.initializeDatabase();
PreparedStatementpst=con.prepareStatement("insertintopatientvalues(?,?,?,?,?,?,?,?,?)");
pst.setString(9,phone);
pst.setString(1,fname);
pst.setString(2,lname);
pst.setString(3,gender);
pst.setString(4,city);
pst.setString(5,email);
pst.setString(6,age);
pst.setString(7,address);
pst.setString(8,DateAndTime);

i=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('LoginSuccessfully..!');");
pw.println("window.location.href=\"UserHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("UserHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('IncorrectData..!');");
pw.println("window.location.href=\"addpatient.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("addpatient.jsp");
//rd.forward(request,response);
}
}catch(SQLExceptionex){
Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE,null,ex);
}catch(ClassNotFoundExceptionex){
Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE,null,ex);
}

}

}
```

#### Controller::updatePatient
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.updatePatient.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/updatePatient.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        
        String fname = request.getParameter("fname");
        String lname = request.getParameter("lname");
        String gender = request.getParameter("gender");
        String phone = request.getParameter("Mobile");
        String city = request.getParameter("City");
        String email = request.getParameter("email");
        String age = request.getParameter("age");
        String address = request.getParameter("address");

        try {
            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("update patient set fname = ? , lname = ? , gender = ? , city = ? , email = ? , age = ? , address = ?  where mobile = '" + phone + "' ");
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, gender);
            pst.setString(4, city);
            pst.setString(5, email);
            pst.setString(6, age);
            pst.setString(7, address);

            int i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Update Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Failed..! Try Again Later...');");
                pw.println("window.location.href = \"updatePatient.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("updatePatient.jsp");
                //rd.forward(request, response);
            }
            con.close();
        } catch (Exception e) {

        }

    }
```

#### AddRecp.java
- AddRecp.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjava.sql.SQLException;
importjava.text.DateFormat;
importjava.text.SimpleDateFormat;
importjava.util.Date;
importjava.util.logging.Level;
importjava.util.logging.Logger;
importjavax.servlet.RequestDispatcher;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/AddRecp")
publicclassAddRecpextendsHttpServlet{

privateinti;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
DatetodaysDate=newDate();
DateFormatdf2=newSimpleDateFormat("dd-MM-yyyyHH:mm:ss");

Stringfname=request.getParameter("fname");
Stringlname=request.getParameter("lname");
Stringphone=request.getParameter("Mobile");
StringDateAndTime=df2.format(todaysDate);

Connectioncon=DatabaseConnection.initializeDatabase();
PreparedStatementpst=con.prepareStatement("insertintorecpvalues(?,?,?,?)");
pst.setString(1,fname);
pst.setString(2,lname);
pst.setString(3,phone);
pst.setString(4,DateAndTime);

i=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('AddSuccessfully..!');");
pw.println("window.location.href=\"AdminHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AdminHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('IncorrectData...!');");
pw.println("window.location.href=\"AddRecp.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AddRecp.jsp");
//rd.forward(request,response);
}
}catch(SQLException|ClassNotFoundExceptionex){
Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE,null,ex);
}
}
}
```

#### Controller::AddWorker
- i
  - Description: i
  - Definition: int Controller.AddWorker.i
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddWorker.java
  - Source Code:
```java
    private int i;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String phone = request.getParameter("Mobile");
            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into worker values(?,?,?,?)");
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, phone);
            pst.setString(4, DateAndTime);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Add Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Incorrect Data..!');");
                pw.println("window.location.href = \"AddWorker.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AddWorker.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.AddWorker.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AddWorker.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
PrintWriter pw = response.getWriter();
        try {
            Date todaysDate = new Date();
            DateFormat df2 = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            String fname = request.getParameter("fname");
            String lname = request.getParameter("lname");
            String phone = request.getParameter("Mobile");
            String DateAndTime = df2.format(todaysDate);

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into worker values(?,?,?,?)");
            pst.setString(1, fname);
            pst.setString(2, lname);
            pst.setString(3, phone);
            pst.setString(4, DateAndTime);

            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Add Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Incorrect Data..!');");
                pw.println("window.location.href = \"AddWorker.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AddWorker.jsp");
                //rd.forward(request, response);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
```

#### AddWorker.java
- AddWorker.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjava.sql.SQLException;
importjava.text.DateFormat;
importjava.text.SimpleDateFormat;
importjava.util.Date;
importjava.util.logging.Level;
importjava.util.logging.Logger;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/AddWorker")
publicclassAddWorkerextendsHttpServlet{

privateinti;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
DatetodaysDate=newDate();
DateFormatdf2=newSimpleDateFormat("dd-MM-yyyyHH:mm:ss");

Stringfname=request.getParameter("fname");
Stringlname=request.getParameter("lname");
Stringphone=request.getParameter("Mobile");
StringDateAndTime=df2.format(todaysDate);

Connectioncon=DatabaseConnection.initializeDatabase();
PreparedStatementpst=con.prepareStatement("insertintoworkervalues(?,?,?,?)");
pst.setString(1,fname);
pst.setString(2,lname);
pst.setString(3,phone);
pst.setString(4,DateAndTime);

i=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('AddSuccessfully..!');");
pw.println("window.location.href=\"AdminHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AdminHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('IncorrectData..!');");
pw.println("window.location.href=\"AddWorker.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AddWorker.jsp");
//rd.forward(request,response);
}
}catch(SQLException|ClassNotFoundExceptionex){
Logger.getLogger(AddPatient.class.getName()).log(Level.SEVERE,null,ex);
}
}
}
```

### Cluster 7
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### Database::DatabaseConnection
- initializeDatabase
  - Description: initializeDatabase()
  - Definition: static Connection Database.DatabaseConnection.initializeDatabase
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Database/DatabaseConnection.java
  - Source Code:
```java
    public static Connection initializeDatabase() 
        throws SQLException, ClassNotFoundException 
    { 
        // Initialize all the information regarding 
        // Database Connection 
        String dbDriver = "com.mysql.jdbc.Driver"; 
        String dbURL = "jdbc:mysql://localhost:3306/"; 
        // Database name to access 
        String dbName = "hospital"; 
        String dbUsername = "root"; 
        String dbPassword = "root"; 
  
        Class.forName(dbDriver); 
        Connection con = DriverManager.getConnection(dbURL+dbName,dbUsername,dbPassword); 
        return con; 
    } 
```

#### deletePatient.jsp
- deletePatient.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:deletePatient
Createdon:19Aug,2020,5:52:13PM
Author:Admin
--%>

<%pageimport="java.sql.Statement"%>
<%pageimport="java.sql.Connection"%>
<%pageimport="Database.DatabaseConnection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>DeletePatient</title>
</head>
<body>
<%
Stringmob=request.getParameter("mob");
Connectioncon=null;
Statementstmt=null;
con=DatabaseConnection.initializeDatabase();
stmt=(Statement)con.createStatement();
Stringquery="deletefrompatient"+"wheremobile='"+mob+"'";
stmt.executeUpdate(query);
con.close();
RequestDispatcherrd=request.getRequestDispatcher("AdminHome.jsp");
rd.forward(request,response);
%>
</body>
</html>
```

#### DatabaseConnection.java
- DatabaseConnection.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageDatabase;

importjava.sql.Connection;
importjava.sql.DriverManager;
importjava.sql.SQLException;

//Thisclasscanbeusedtoinitializethedatabaseconnection
publicclassDatabaseConnection{
publicstaticConnectioninitializeDatabase()
throwsSQLException,ClassNotFoundException
{
//Initializealltheinformationregarding
//DatabaseConnection
StringdbDriver="com.mysql.jdbc.Driver";
StringdbURL="jdbc:mysql://localhost:3306/";
//Databasenametoaccess
StringdbName="hospital";
StringdbUsername="root";
StringdbPassword="root";

Class.forName(dbDriver);
Connectioncon=DriverManager.getConnection(dbURL+dbName,dbUsername,dbPassword);
returncon;
}
}
```

#### project.xml
- project.xml
  - Description: Code from programlisting
  - Source Code:
```java
<?xmlversion="1.0"encoding="UTF-8"?>
<projectxmlns="http://www.netbeans.org/ns/project/1">
<type>org.netbeans.modules.web.project</type>
<configuration>
<dataxmlns="http://www.netbeans.org/ns/web-project/3">
<name>HospitalManagementSystem</name>
<minimum-ant-version>1.6.5</minimum-ant-version>
<web-module-libraries>
<librarydirs="200">
<file>${file.reference.jstl-1.2.jar}</file>
<path-in-war>WEB-INF/lib</path-in-war>
</library>
<librarydirs="200">
<file>${file.reference.mysql-connector-java-5.1.5-bin.jar}</file>
<path-in-war>WEB-INF/lib</path-in-war>
</library>
<librarydirs="200">
<file>${file.reference.taglibs-standard-impl-1.2.5.jar}</file>
<path-in-war>WEB-INF/lib</path-in-war>
</library>
</web-module-libraries>
<web-module-additional-libraries/>
<source-roots>
<rootid="src.dir"name="SourcePackages"/>
</source-roots>
<test-roots>
<rootid="test.src.dir"name="TestPackages"/>
</test-roots>
</data>
</configuration>
</project>
```

### Cluster 0
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### AdminLogin.java
- AdminLogin.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.ResultSet;
importjava.sql.Statement;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/AdminLogin")
publicclassAdminLoginextendsHttpServlet{

privateStringuser;
privateStringpass;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
Stringuserp=request.getParameter("your_name");
Stringpassp=request.getParameter("your_pass");
Connectioncon=DatabaseConnection.initializeDatabase();

Strings="select*fromadminreg";
Statementst=con.createStatement();
ResultSetrs=st.executeQuery(s);
while(rs.next()){
user=rs.getString(1);
pass=rs.getString(2);
}
if(userp.equals(user)&&passp.equals(pass)){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('LoginSuccessfully..!');");
pw.println("window.location.href=\"AdminHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("AdminHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('UsernameorPasswordisIncorrect..!');");
pw.println("window.location.href=\"index.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("index.jsp");
//rd.include(request,response);
}
}catch(Exceptione){

}

}

}
```

#### Controller::UserLogin
- user
  - Description: user
  - Definition: String Controller.UserLogin.user
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserLogin.java
  - Source Code:
```java
    private String user;
    private String pass;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("username");
            String passp = request.getParameter("password");
            Connection con = DatabaseConnection.initializeDatabase();

            String s = "select *from login";
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(s);
            while (rs.next()) {
                user = rs.getString(1);
                pass = rs.getString(2);
            }
            if (userp.equals(user) && passp.equals(pass)) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"UserHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("UserHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                // RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                // rd.include(request, response);
            }
        } catch (Exception e) {

        }

    }

```
- pass
  - Description: pass
  - Definition: String Controller.UserLogin.pass
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserLogin.java
  - Source Code:
```java
    private String pass;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("username");
            String passp = request.getParameter("password");
            Connection con = DatabaseConnection.initializeDatabase();

            String s = "select *from login";
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(s);
            while (rs.next()) {
                user = rs.getString(1);
                pass = rs.getString(2);
            }
            if (userp.equals(user) && passp.equals(pass)) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"UserHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("UserHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                // RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                // rd.include(request, response);
            }
        } catch (Exception e) {

        }

    }

```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.UserLogin.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserLogin.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("username");
            String passp = request.getParameter("password");
            Connection con = DatabaseConnection.initializeDatabase();

            String s = "select *from login";
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(s);
            while (rs.next()) {
                user = rs.getString(1);
                pass = rs.getString(2);
            }
            if (userp.equals(user) && passp.equals(pass)) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"UserHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("UserHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                // RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                // rd.include(request, response);
            }
        } catch (Exception e) {

        }

    }
```

#### UserLogin.java
- UserLogin.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.ResultSet;
importjava.sql.Statement;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/UserLogin")
publicclassUserLoginextendsHttpServlet{

privateStringuser;
privateStringpass;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
Stringuserp=request.getParameter("username");
Stringpassp=request.getParameter("password");
Connectioncon=DatabaseConnection.initializeDatabase();

Strings="select*fromlogin";
Statementst=con.createStatement();
ResultSetrs=st.executeQuery(s);
while(rs.next()){
user=rs.getString(1);
pass=rs.getString(2);
}
if(userp.equals(user)&&passp.equals(pass)){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('LoginSuccessfully..!');");
pw.println("window.location.href=\"UserHome.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("UserHome.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('UsernameorPasswordisIncorrect..!');");
pw.println("window.location.href=\"index.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("index.jsp");
//rd.include(request,response);
}
}catch(Exceptione){

}

}

}
```

#### Controller::AdminLogin
- user
  - Description: user
  - Definition: String Controller.AdminLogin.user
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AdminLogin.java
  - Source Code:
```java
    private String user;
    private String pass;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("your_name");
            String passp = request.getParameter("your_pass");
            Connection con = DatabaseConnection.initializeDatabase();

            String s = "select *from adminreg";
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(s);
            while (rs.next()) {
                user = rs.getString(1);
                pass = rs.getString(2);
            }
            if (userp.equals(user) && passp.equals(pass)) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.include(request, response);
            }
        } catch (Exception e) {

        }

    }

```
- pass
  - Description: pass
  - Definition: String Controller.AdminLogin.pass
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AdminLogin.java
  - Source Code:
```java
    private String pass;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("your_name");
            String passp = request.getParameter("your_pass");
            Connection con = DatabaseConnection.initializeDatabase();

            String s = "select *from adminreg";
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(s);
            while (rs.next()) {
                user = rs.getString(1);
                pass = rs.getString(2);
            }
            if (userp.equals(user) && passp.equals(pass)) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.include(request, response);
            }
        } catch (Exception e) {

        }

    }

```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.AdminLogin.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AdminLogin.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("your_name");
            String passp = request.getParameter("your_pass");
            Connection con = DatabaseConnection.initializeDatabase();

            String s = "select *from adminreg";
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(s);
            while (rs.next()) {
                user = rs.getString(1);
                pass = rs.getString(2);
            }
            if (userp.equals(user) && passp.equals(pass)) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Login Successfully..!');");
                pw.println("window.location.href = \"AdminHome.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("AdminHome.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.include(request, response);
            }
        } catch (Exception e) {

        }

    }
```

#### Controller::AdminRegister
- i
  - Description: i
  - Definition: int Controller.AdminRegister.i
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AdminRegister.java
  - Source Code:
```java
    private int i = 0;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("email");
            String passp = request.getParameter("pass");
            String rpassp = request.getParameter("re_pass");
            String tikbox = request.getParameter("agree-term");

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into adminreg values(?,?)");
            pst.setString(1, userp);
            pst.setString(2, passp);
            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Registerd Successfully..!');");
                pw.println("window.location.href = \"adminLogin.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("adminLogin.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"adminRegister.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("adminRegister.jsp");
                //rd.forward(request, response);
            }

        } catch (Exception e) {

        }

    }

```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.AdminRegister.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/AdminRegister.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            String userp = request.getParameter("email");
            String passp = request.getParameter("pass");
            String rpassp = request.getParameter("re_pass");
            String tikbox = request.getParameter("agree-term");

            Connection con = DatabaseConnection.initializeDatabase();
            PreparedStatement pst = con.prepareStatement("insert into adminreg values(?,?)");
            pst.setString(1, userp);
            pst.setString(2, passp);
            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Registerd Successfully..!');");
                pw.println("window.location.href = \"adminLogin.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("adminLogin.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Username or Password is Incorrect..!');");
                pw.println("window.location.href = \"adminRegister.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("adminRegister.jsp");
                //rd.forward(request, response);
            }

        } catch (Exception e) {

        }

    }
```

#### AdminRegister.java
- AdminRegister.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjavax.servlet.RequestDispatcher;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/AdminRegister")
publicclassAdminRegisterextendsHttpServlet{

privateinti=0;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
Stringuserp=request.getParameter("email");
Stringpassp=request.getParameter("pass");
Stringrpassp=request.getParameter("re_pass");
Stringtikbox=request.getParameter("agree-term");

Connectioncon=DatabaseConnection.initializeDatabase();
PreparedStatementpst=con.prepareStatement("insertintoadminregvalues(?,?)");
pst.setString(1,userp);
pst.setString(2,passp);
i=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('RegisterdSuccessfully..!');");
pw.println("window.location.href=\"adminLogin.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("adminLogin.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('UsernameorPasswordisIncorrect..!');");
pw.println("window.location.href=\"adminRegister.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("adminRegister.jsp");
//rd.forward(request,response);
}

}catch(Exceptione){

}

}

}
```

### Cluster 9
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### Controller::UserRegister
- user
  - Description: user
  - Definition: String Controller.UserRegister.user
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserRegister.java
  - Source Code:
```java
    private String user;
    private String pass;
    private int i = 0;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Connection con = DatabaseConnection.initializeDatabase();

            user = request.getParameter("Username");
            pass = request.getParameter("password");
            String repassp = request.getParameter("repassword");

            PreparedStatement pst = con.prepareStatement("insert into login values(?,?)");
            pst.setString(1, user);
            pst.setString(2, pass);
            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Successfully..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Failed');");
                pw.println("window.location.href = \"userRegister.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("userRegister.jsp");
                //rd.forward(request, response);
            }

        } catch (Exception e) {

        }

    }

```
- pass
  - Description: pass
  - Definition: String Controller.UserRegister.pass
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserRegister.java
  - Source Code:
```java
    private String pass;
    private int i = 0;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Connection con = DatabaseConnection.initializeDatabase();

            user = request.getParameter("Username");
            pass = request.getParameter("password");
            String repassp = request.getParameter("repassword");

            PreparedStatement pst = con.prepareStatement("insert into login values(?,?)");
            pst.setString(1, user);
            pst.setString(2, pass);
            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Successfully..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Failed');");
                pw.println("window.location.href = \"userRegister.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("userRegister.jsp");
                //rd.forward(request, response);
            }

        } catch (Exception e) {

        }

    }

```
- i
  - Description: i
  - Definition: int Controller.UserRegister.i
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserRegister.java
  - Source Code:
```java
    private int i = 0;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Connection con = DatabaseConnection.initializeDatabase();

            user = request.getParameter("Username");
            pass = request.getParameter("password");
            String repassp = request.getParameter("repassword");

            PreparedStatement pst = con.prepareStatement("insert into login values(?,?)");
            pst.setString(1, user);
            pst.setString(2, pass);
            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Successfully..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Failed');");
                pw.println("window.location.href = \"userRegister.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("userRegister.jsp");
                //rd.forward(request, response);
            }

        } catch (Exception e) {

        }

    }

```
- doPost
  - Description: doPost(HttpServletRequest request, HttpServletResponse response)
  - Definition: void Controller.UserRegister.doPost
  - Source File: /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem/src/java/Controller/UserRegister.java
  - Source Code:
```java
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter pw = response.getWriter();
        try {
            Connection con = DatabaseConnection.initializeDatabase();

            user = request.getParameter("Username");
            pass = request.getParameter("password");
            String repassp = request.getParameter("repassword");

            PreparedStatement pst = con.prepareStatement("insert into login values(?,?)");
            pst.setString(1, user);
            pst.setString(2, pass);
            i = pst.executeUpdate();
            if (i > 0) {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Successfully..!');");
                pw.println("window.location.href = \"index.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("index.jsp");
                //rd.forward(request, response);
            } else {
                pw.println("<script type=\"text/javascript\">");
                pw.println("alert('Register Failed');");
                pw.println("window.location.href = \"userRegister.jsp\";");
                pw.println("</script>");
                //RequestDispatcher rd = request.getRequestDispatcher("userRegister.jsp");
                //rd.forward(request, response);
            }

        } catch (Exception e) {

        }

    }
```

#### UserRegister.java
- UserRegister.java
  - Description: Code from programlisting
  - Source Code:
```java
/*
*Tochangethislicenseheader,chooseLicenseHeadersinProjectProperties.
*Tochangethistemplatefile,chooseTools|Templates
*andopenthetemplateintheeditor.
*/
packageController;

importDatabase.DatabaseConnection;
importjava.io.IOException;
importjava.io.PrintWriter;
importjava.sql.Connection;
importjava.sql.PreparedStatement;
importjavax.servlet.ServletException;
importjavax.servlet.annotation.WebServlet;
importjavax.servlet.http.HttpServlet;
importjavax.servlet.http.HttpServletRequest;
importjavax.servlet.http.HttpServletResponse;

WebServlet("/UserRegister")
publicclassUserRegisterextendsHttpServlet{

privateStringuser;
privateStringpass;
privateinti=0;

Override
protectedvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse)
throwsServletException,IOException{
PrintWriterpw=response.getWriter();
try{
Connectioncon=DatabaseConnection.initializeDatabase();

user=request.getParameter("Username");
pass=request.getParameter("password");
Stringrepassp=request.getParameter("repassword");

PreparedStatementpst=con.prepareStatement("insertintologinvalues(?,?)");
pst.setString(1,user);
pst.setString(2,pass);
i=pst.executeUpdate();
if(i>0){
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('RegisterSuccessfully..!');");
pw.println("window.location.href=\"index.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("index.jsp");
//rd.forward(request,response);
}else{
pw.println("<scripttype=\"text/javascript\">");
pw.println("alert('RegisterFailed');");
pw.println("window.location.href=\"userRegister.jsp\";");
pw.println("</script>");
//RequestDispatcherrd=request.getRequestDispatcher("userRegister.jsp");
//rd.forward(request,response);
}

}catch(Exceptione){

}

}

}
```

### Cluster 4
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### adminDoctorList.jsp
- adminDoctorList.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:15Aug,2020,3:56:36AM
Author:Admin
--%>

<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.Statement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pageimport="java.sql.Connection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>PatientList</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<linkrel="stylesheet"type="text/css"href="css/table.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
.serchbar
{
width:60%;
height:5%;
margin-top:2%;
margin-left:100px;
margin-bottom:0%;
}
.search
{
width:40%;
height:40px;
border-radius:10px;
}
.text-center{
color:grey;
padding:10px;
margin-top:0px;
}
input{
text-align:center;
}
::-webkit-input-placeholder{
text-align:center;
}
:-moz-placeholder{
text-align:center;
}
.mybutton{
display:inline;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptonist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptonist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>

<divclass="serchbar">
<formaction=""method="post">
<inputclass="search"type="text"name="search"placeholder="SearchHere..."/>
</form>
</div>



<%
Connectioncon=null;
%>
<div>
<divclass="container-table100">
<divclass="wrap-table100">
<divclass="table100ver3m-b-110">
<divclass="table100-head">
<table>
<thead>
<trclass="row100head">
<thclass="cell100column0">Id</th>
<thclass="cell100column1">FirstName</th>
<thclass="cell100column2">LastName</th>
<thclass="cell100column3">Gender</th>
<thclass="cell100column4">Mobile</th>
<thclass="cell100column5">City</th>
<thclass="cell100column6">Email</th>
<thclass="cell100column7">Age</th>
<thclass="cell100column8">Address</th>
<thclass="cell100column9">Date</th>
<thclass="cell100column10">Qualification</th>
</tr>
</thead>
</table>
</div>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringsql="";
Stringquery=request.getParameter("search");
if(query!=null){
sql="select*fromdoctorwherefnamelike'%"+query+"%'orlnamelike'%"+query+"%'";
}else{
sql="select*fromdoctor";
}
ResultSetrs=st.executeQuery(sql);
while(rs.next()){
%>
<divclass="table100-bodyjs-pscroll">
<table>
<tbody>
<trclass="row100body">
<tdclass="cell100column0"><%=rs.getInt(1)%></td>
<tdclass="cell100column1"><%=rs.getString(2)%></td>
<tdclass="cell100column2"><%=rs.getString(3)%></td>
<tdclass="cell100column3"><%=rs.getString(4)%></td>
<tdclass="cell100column4"><%=rs.getString(5)%></td>
<tdclass="cell100column5"><%=rs.getString(6)%></td>
<tdclass="cell100column6"><%=rs.getString(7)%></td>
<tdclass="cell100column7"><%=rs.getString(8)%></td>
<tdclass="cell100column8"><%=rs.getString(9)%></td>
<tdclass="cell100column9"><%=rs.getString(10)%></td>
<tdclass="cell100column10"><%=rs.getString(11)%></td>
<td>
<ahref="addpatient.jsp">Edit</a>
&nbsp;&nbsp;&nbsp;&nbsp;
<ahref="">Delete</a>
</td>
</tr>
</tbody>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
</table>
</div>
</div>
</div>
</div>
</div>



</body>
</html>
```

#### adminRecpList.jsp
- adminRecpList.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:15Aug,2020,3:56:36AM
Author:Admin
--%>

<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.Statement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pageimport="java.sql.Connection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>PatientList</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<linkrel="stylesheet"type="text/css"href="css/table.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
.serchbar
{
width:60%;
height:5%;
margin-top:2%;
margin-left:100px;
margin-bottom:0%;
}
.search
{
width:40%;
height:40px;
border-radius:10px;
}
.text-center{
color:grey;
padding:10px;
margin-top:0px;
}
input{
text-align:center;
}
::-webkit-input-placeholder{
text-align:center;
}
:-moz-placeholder{
text-align:center;
}
.mybutton{
display:inline;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptonist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptonist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>

<divclass="serchbar">
<formaction=""method="post">
<inputclass="search"type="text"name="search"placeholder="SearchHere..."/>
</form>
</div>



<%
Connectioncon=null;
%>
<div>
<divclass="container-table100">
<divclass="wrap-table100">
<divclass="table100ver3m-b-110">
<divclass="table100-head">
<table>
<thead>
<trclass="row100head">
<thclass="cell100column1">FirstName</th>
<thclass="cell100column2">LastName</th>
<thclass="cell100column3">Mobile</th>
<thclass="cell100column4">Date</th>
<thclass="cell100column5">Action</th>
</tr>
</thead>
</table>
</div>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringsql="";
Stringquery=request.getParameter("search");
if(query!=null){
sql="select*fromrecpwherefnamelike'%"+query+"%'orlnamelike'%"+query+"%'";
}else{
sql="select*fromrecp";
}
ResultSetrs=st.executeQuery(sql);
while(rs.next()){
%>
<divclass="table100-bodyjs-pscroll">
<table>
<tbody>
<trclass="row100body">
<tdclass="cell100column1"><%=rs.getString(1)%></td>
<tdclass="cell100column2"><%=rs.getString(2)%></td>
<tdclass="cell100column3"><%=rs.getString(3)%></td>
<tdclass="cell100column4"><%=rs.getString(4)%></td>
<tdclass="cell100column5">
<ahref="">Edit</a>
&nbsp;&nbsp;&nbsp;&nbsp;
<ahref="">Delete</a>
</td>
</tr>
</tbody>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
</table>
</div>
</div>
</div>
</div>
</div>



</body>
</html>
```

#### listPatient.jsp
- listPatient.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:15Aug,2020,3:56:36AM
Author:Admin
--%>

<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.Statement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pageimport="java.sql.Connection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>PatientList</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<linkrel="stylesheet"type="text/css"href="css/table.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
.serchbar
{
width:60%;
height:5%;
margin-top:2%;
margin-left:100px;
margin-bottom:0%;
}
.search
{
width:40%;
height:40px;
border-radius:10px;
}
.text-center{
color:grey;
padding:10px;
margin-top:0px;
}
input{
text-align:center;
}
::-webkit-input-placeholder{
text-align:center;
}
:-moz-placeholder{
text-align:center;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<ulclass="navbar-navmr-auto">
<liclass="nav-itemactive">
<aclass="nav-link"href="index.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="listPatient.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
Billing
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="#">AddBill</a>
<aclass="dropdown-item"href="#">ViewBill</a>
</div>
</li>
</ul>
</div>
</nav>

<divclass="serchbar">
<formaction=""method="post">
<inputclass="search"type="text"name="search"placeholder="SearchHere..."/>
</form>
</div>
<%
Connectioncon=null;
%>
<div>
<divclass="container-table100">
<divclass="wrap-table100">
<divclass="table100ver3m-b-110">
<divclass="table100-head">
<table>
<thead>
<trclass="row100head">
<thclass="cell100column1">FirstName</th>
<thclass="cell100column2">LastName</th>
<thclass="cell100column3">Gender</th>
<thclass="cell100column4">City</th>
<thclass="cell100column5">Email</th>
<thclass="cell100column6">Age</th>
<thclass="cell100column7">Address</th>
<thclass="cell100column8">Date</th>
<thclass="cell100column9">Mobile</th>
</tr>
</thead>
</table>
</div>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringsql="";
Stringquery=request.getParameter("search");
if(query!=null){
sql="select*frompatientwherefnamelike'%"+query+"%'orlnamelike'%"+query+"%'";
}else{
sql="select*frompatient";
}
ResultSetrs=st.executeQuery(sql);
while(rs.next()){
%>
<divclass="table100-bodyjs-pscroll">
<table>
<tbody>
<trclass="row100body">
<tdclass="cell100column1"><%=rs.getString(1)%></td>
<tdclass="cell100column2"><%=rs.getString(2)%></td>
<tdclass="cell100column3"><%=rs.getString(3)%></td>
<tdclass="cell100column4"><%=rs.getString(4)%></td>
<tdclass="cell100column5"><%=rs.getString(5)%></td>
<tdclass="cell100column6"><%=rs.getString(6)%></td>
<tdclass="cell100column7"><%=rs.getString(7)%></td>
<tdclass="cell100column8"><%=rs.getString(8)%></td>
<tdclass="cell100column9"><%=rs.getString(9)%></td>
</tr>
</tbody>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
</table>
</div>
</div>
</div>
</div>
</div>



</body>
</html>
```

#### adminPatientList.jsp
- adminPatientList.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:15Aug,2020,3:56:36AM
Author:Admin
--%>

<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.Statement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pageimport="java.sql.Connection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>PatientList</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<linkrel="stylesheet"type="text/css"href="css/table.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
.serchbar
{
width:60%;
height:5%;
margin-top:2%;
margin-left:100px;
margin-bottom:0%;
}
.search
{
width:40%;
height:40px;
border-radius:10px;
}
.text-center{
color:grey;
padding:10px;
margin-top:0px;
}
input{
text-align:center;
}
::-webkit-input-placeholder{
text-align:center;
}
:-moz-placeholder{
text-align:center;
}
.mybutton{
display:inline;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptonist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptonist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>

<divclass="serchbar">
<formaction=""method="post">
<inputclass="search"type="text"name="search"placeholder="SearchHere..."/>
</form>
</div>



<%
Connectioncon=null;
%>
<div>
<divclass="container-table100">
<divclass="wrap-table100">
<divclass="table100ver3m-b-110">
<divclass="table100-head">
<table>
<thead>
<trclass="row100head">
<thclass="cell100column1">FirstName</th>
<thclass="cell100column2">LastName</th>
<thclass="cell100column3">Gender</th>
<thclass="cell100column4">City</th>
<thclass="cell100column5">Email</th>
<thclass="cell100column6">Age</th>
<thclass="cell100column7">Address</th>
<thclass="cell100column8">Date</th>
<thclass="cell100column9">Mobile</th>
<thclass="cell100column10">Action</th>
</tr>
</thead>
</table>
</div>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringsql="";
Stringquery=request.getParameter("search");
if(query!=null){
sql="select*frompatientwherefnamelike'%"+query+"%'orlnamelike'%"+query+"%'";
}else{
sql="select*frompatient";
}
ResultSetrs=st.executeQuery(sql);
while(rs.next()){
Stringmob=rs.getString(9);
%>
<divclass="table100-bodyjs-pscroll">
<table>
<tbody>
<trclass="row100body">
<tdclass="cell100column1"><%=rs.getString(1)%></td>
<tdclass="cell100column2"><%=rs.getString(2)%></td>
<tdclass="cell100column3"><%=rs.getString(3)%></td>
<tdclass="cell100column4"><%=rs.getString(4)%></td>
<tdclass="cell100column5"><%=rs.getString(5)%></td>
<tdclass="cell100column6"><%=rs.getString(6)%></td>
<tdclass="cell100column7"><%=rs.getString(7)%></td>
<tdclass="cell100column8"><%=rs.getString(8)%></td>
<tdclass="cell100column9"><%=rs.getString(9)%></td>
<tdclass="cell100column10">
<ahref="updatePatient.jsp?mob=<%=mob%>">Edit</a>
&nbsp;&nbsp;&nbsp;&nbsp;
<ahref="deletePatient.jsp?mob=<%=mob%>">Delete</a>
</td>
</tr>
</tbody>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
</table>
</div>
</div>
</div>
</div>
</div>



</body>
</html>
```

#### adminWorkerList.jsp
- adminWorkerList.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:adminWorkerList
Createdon:15Aug,2020,3:56:36AM
Author:Admin
--%>

<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.Statement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pageimport="java.sql.Connection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>PatientList</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<linkrel="stylesheet"type="text/css"href="css/table.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
.serchbar
{
width:60%;
height:5%;
margin-top:2%;
margin-left:100px;
margin-bottom:0%;
}
.search
{
width:40%;
height:40px;
border-radius:10px;
}
.text-center{
color:grey;
padding:10px;
margin-top:0px;
}
input{
text-align:center;
}
::-webkit-input-placeholder{
text-align:center;
}
:-moz-placeholder{
text-align:center;
}
.mybutton{
display:inline;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptonist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptonist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>

<divclass="serchbar">
<formaction=""method="post">
<inputclass="search"type="text"name="search"placeholder="SearchHere..."/>
</form>
</div>



<%
Connectioncon=null;
%>
<div>
<divclass="container-table100">
<divclass="wrap-table100">
<divclass="table100ver3m-b-110">
<divclass="table100-head">
<table>
<thead>
<trclass="row100head">
<thclass="cell100column1">FirstName</th>
<thclass="cell100column2">LastName</th>
<thclass="cell100column3">Mobile</th>
<thclass="cell100column4">Date</th>
<thclass="cell100column5">Action</th>
</tr>
</thead>
</table>
</div>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringsql="";
Stringquery=request.getParameter("search");
if(query!=null){
sql="select*fromworkerwherefnamelike'%"+query+"%'orlnamelike'%"+query+"%'";
}else{
sql="select*fromworker";
}
ResultSetrs=st.executeQuery(sql);
while(rs.next()){
%>
<divclass="table100-bodyjs-pscroll">
<table>
<tbody>
<trclass="row100body">
<tdclass="cell100column1"><%=rs.getString(1)%></td>
<tdclass="cell100column2"><%=rs.getString(2)%></td>
<tdclass="cell100column3"><%=rs.getString(3)%></td>
<tdclass="cell100column4"><%=rs.getString(4)%></td>
<tdclass="cell100column5">
<ahref="">Edit</a>
&nbsp;&nbsp;&nbsp;&nbsp;
<ahref="">Delete</a>
</td>
</tr>
</tbody>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
</table>
</div>
</div>
</div>
</div>
</div>



</body>
</html>
```

#### AdminHome.jsp
- AdminHome.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:13Aug,2020,9:56:36AM
Author:Admin
--%>

<%pageimport="java.sql.Connection"%>
<%pageimport="java.sql.ResultSet"%>
<%pageimport="java.sql.Statement"%>
<%pageimport="Database.DatabaseConnection"%>
<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>AdminHome</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
height:100%;
}
body.modal-open{
padding-right:0!important;
}

#sidebar{
padding-left:0;
}
/*
*OffCanvasatmediumbreakpoint
*--------------------------------------------------
*/

mediascreenand(max-width:48em){
.row-offcanvas{
position:relative;
-webkit-transition:all0.25sease-out;
-moz-transition:all0.25sease-out;
transition:all0.25sease-out;
}
.row-offcanvas-left.sidebar-offcanvas{
left:-33%;
}
.row-offcanvas-left.active{
left:33%;
margin-left:-6px;
}
.sidebar-offcanvas{
position:absolute;
top:0;
width:33%;
height:100%;
}
}
/*
*OffCanvaswideratsmbreakpoint
*--------------------------------------------------
*/

mediascreenand(max-width:34em){
.row-offcanvas-left.sidebar-offcanvas{
left:-45%;
}
.row-offcanvas-left.active{
left:45%;
margin-left:-6px;
}
.sidebar-offcanvas{
width:45%;
}
}

.card{
overflow:hidden;
}

.card-block.rotate{
z-index:8;
float:right;
height:100%;
}

.card-block.rotatei{
color:rgba(20,20,20,0.15);
position:absolute;
left:0;
left:auto;
right:-10px;
bottom:0;
display:block;
-webkit-transform:rotate(-44deg);
-moz-transform:rotate(-44deg);
-o-transform:rotate(-44deg);
-ms-transform:rotate(-44deg);
transform:rotate(-44deg);
}
a{
color:white;

}
</style>
</head>
<body>
<%
Connectioncon=null;
%>

<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="index.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptionist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptionist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>

<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringquery="selectcount(*)frompatient";
ResultSetrs=st.executeQuery(query);
while(rs.next()){
intpatient=rs.getInt(1);
%>

<divclass="rowmb-3">
<divclass="col-xl-3col-lg-6"style="margin-top:20px;">
<divclass="cardcard-inversecard-success">
<divclass="card-blockbg-success">
<divclass="rotate">
<iclass="fafa-userfa-5x"></i>
</div>
<h6class="text-uppercase"style="text-align:center;"><ahref="adminPatientList.jsp">Patient</a></h6>
<h1class="display-1"style="text-align:center"><%=patient%></h1>
</div>
</div>
</div>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringquery="selectcount(*)fromdoctor";
ResultSetrs=st.executeQuery(query);
while(rs.next()){
intdoctor=rs.getInt(1);
%>
<divclass="col-xl-3col-lg-6"style="margin-top:20px;">
<divclass="cardcard-inversecard-danger">
<divclass="card-blockbg-danger">
<divclass="rotate">
<iclass="fafa-userfa-5x"></i>
</div>
<h6class="text-uppercase"style="text-align:center"><ahref="adminDoctorList.jsp">Doctor</a></h6>
<h1class="display-1"style="text-align:center"><%=doctor%></h1>
</div>
</div>
</div>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringquery="selectcount(*)fromrecp";
ResultSetrs=st.executeQuery(query);
while(rs.next()){
intrecp=rs.getInt(1);
%>
<divclass="col-xl-3col-lg-6"style="margin-top:20px;">
<divclass="cardcard-inversecard-info">
<divclass="card-blockbg-info">
<divclass="rotate">
<iclass="fafa-userfa-5x"></i>
</div>
<h6class="text-uppercase"style="text-align:center"><ahref="adminRecpList.jsp">Receptionist</a></h6>
<h1class="display-1"style="text-align:center"><%=recp%></h1>
</div>
</div>
</div>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>
<%
try{
con=DatabaseConnection.initializeDatabase();
Statementst=(Statement)con.createStatement();
Stringquery="selectcount(*)fromworker";
ResultSetrs=st.executeQuery(query);
while(rs.next()){
intworker=rs.getInt(1);
%>
<divclass="col-xl-3col-lg-6"style="margin-top:20px;">
<divclass="cardcard-inversecard-warning">
<divclass="card-blockbg-warning">
<divclass="rotate">
<iclass="fafa-userfa-5x"></i>
</div>
<h6class="text-uppercase"style="text-align:center"><ahref="adminWorkerList.jsp">Worker</a></h6>
<h1class="display-1"style="text-align:center"><%=worker%></h1>
</div>
</div>
</div>
</div>
<%
}
con.close();
}catch(Exceptione){
e.printStackTrace();
}
%>

</body>
</html>
```

### Cluster 1
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### addpatient.jsp
- addpatient.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:13Aug,2020,9:56:36AM
Author:Admin
--%>

<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>UserHome</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<ulclass="navbar-navmr-auto">
<liclass="nav-itemactive">
<aclass="nav-link"href="index.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="listPatient.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
Billing
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="#">AddBill</a>
<aclass="dropdown-item"href="#">ViewBill</a>
</div>
</li>
</ul>
</div>
</nav>


<divclass="container-contact100">


<divclass="wrap-contact100">
<divclass="contact100-form-title"style="background-image:url(img/bg-01.jpg);">
<spanclass="contact100-form-title-1">
PatientRegistrationForm
</span>
</div>

<formclass="contact100-formvalidate-form"action="<%=request.getContextPath()%>/AddPatient"method="post">
<divclass="wrap-input100validate-input"data-validate="FirstNameisrequired">
<spanclass="label-input100">First_Name:</span>
<inputclass="input100"type="text"name="fname"placeholder="EnterFirstname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="LastNameisrequired">
<spanclass="label-input100">Last_Name:</span>
<inputclass="input100"type="text"name="lname"placeholder="EnterLastname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="genderisrequired">
<spanclass="label-input100">Gender:</span>
<inputclass="input100"type="text"name="gender"placeholder="EnterGender">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Phoneisrequired">
<spanclass="label-input100">Phone:</span>
<inputclass="input100"type="text"name="Mobile"placeholder="Enterphonenumber">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Cityisrequired">
<spanclass="label-input100">City:</span>
<inputclass="input100"type="text"name="City"placeholder="EnterCity">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Validemailisrequired:exabc.xyz">
<spanclass="label-input100">Email:</span>
<inputclass="input100"type="text"name="email"placeholder="Enteremail">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Ageisrequired">
<spanclass="label-input100">Age:</span>
<inputclass="input100"type="text"name="age"placeholder="EnterAge">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Addressisrequired">
<spanclass="label-input100">Address</span>
<inputclass="input100"type="text"name="address"placeholder="EnterAddress">
<spanclass="focus-input100"></span>
</div>

<divclass="container-contact100-form-btn">
<buttonclass="contact100-form-btn">
<span>
Submit
<iclass="fafa-long-arrow-rightm-l-7"aria-hidden="true"></i>
</span>
</button>
</div>
</form>
</div>
</div>



<divid="dropDownSelect1"></div>
<scriptsrc="https://maps.googleapis.com/maps/api/js?key=AIzaSyAKFWBqlKAGCeS1rMVoaNlwyayu0e0YRes"></script>
<scriptsrc="js/map-custom.js"></script>
<!--===============================================================================================-->
<scriptsrc="js/main.js"></script>

<!--Globalsitetag(gtag.js)-GoogleAnalytics-->
<scriptasyncsrc="https://www.googletagmanager.com/gtag/js?id=UA-23581568-13"></script>
<script>
window.dataLayer=window.dataLayer||[];
functiongtag(){
dataLayer.push(arguments);
}
gtag('js',newDate());

gtag('config','UA-23581568-13');
</script>


</body>
</html>
```

#### addWorker.jsp
- addWorker.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:13Aug,2020,9:56:36AM
Author:Admin
--%>

<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>UserHome</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptionist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptionist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>


<divclass="container-contact100">


<divclass="wrap-contact100">
<divclass="contact100-form-title"style="background-image:url(img/bg-01.jpg);">
<spanclass="contact100-form-title-1">
ReceptionistRegistrationForm
</span>
</div>

<formclass="contact100-formvalidate-form"action="<%=request.getContextPath()%>/AddWorker"method="post">

<divclass="wrap-input100validate-input"data-validate="FirstNameisrequired">
<spanclass="label-input100">First_Name:</span>
<inputclass="input100"type="text"name="fname"placeholder="EnterFirstname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="LastNameisrequired">
<spanclass="label-input100">Last_Name:</span>
<inputclass="input100"type="text"name="lname"placeholder="EnterLastname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Phoneisrequired">
<spanclass="label-input100">Phone:</span>
<inputclass="input100"type="text"name="Mobile"placeholder="Enterphonenumber">
<spanclass="focus-input100"></span>
</div>

<divclass="container-contact100-form-btn">
<buttonclass="contact100-form-btn">
<span>
Submit
<iclass="fafa-long-arrow-rightm-l-7"aria-hidden="true"></i>
</span>
</button>
</div>
</form>
</div>
</div>



<divid="dropDownSelect1"></div>
<scriptsrc="https://maps.googleapis.com/maps/api/js?key=AIzaSyAKFWBqlKAGCeS1rMVoaNlwyayu0e0YRes"></script>
<scriptsrc="js/map-custom.js"></script>
<!--===============================================================================================-->
<scriptsrc="js/main.js"></script>

<!--Globalsitetag(gtag.js)-GoogleAnalytics-->
<scriptasyncsrc="https://www.googletagmanager.com/gtag/js?id=UA-23581568-13"></script>
<script>
window.dataLayer=window.dataLayer||[];
functiongtag(){
dataLayer.push(arguments);
}
gtag('js',newDate());

gtag('config','UA-23581568-13');
</script>


</body>
</html>
```

#### addRecp.jsp
- addRecp.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:13Aug,2020,9:56:36AM
Author:Admin
--%>

<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>UserHome</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptionist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptionist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>


<divclass="container-contact100">


<divclass="wrap-contact100">
<divclass="contact100-form-title"style="background-image:url(img/bg-01.jpg);">
<spanclass="contact100-form-title-1">
ReceptionistRegistrationForm
</span>
</div>

<formclass="contact100-formvalidate-form"action="<%=request.getContextPath()%>/AddRecp"method="post">

<divclass="wrap-input100validate-input"data-validate="FirstNameisrequired">
<spanclass="label-input100">First_Name:</span>
<inputclass="input100"type="text"name="fname"placeholder="EnterFirstname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="LastNameisrequired">
<spanclass="label-input100">Last_Name:</span>
<inputclass="input100"type="text"name="lname"placeholder="EnterLastname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Phoneisrequired">
<spanclass="label-input100">Phone:</span>
<inputclass="input100"type="text"name="Mobile"placeholder="Enterphonenumber">
<spanclass="focus-input100"></span>
</div>

<divclass="container-contact100-form-btn">
<buttonclass="contact100-form-btn">
<span>
Submit
<iclass="fafa-long-arrow-rightm-l-7"aria-hidden="true"></i>
</span>
</button>
</div>
</form>
</div>
</div>



<divid="dropDownSelect1"></div>
<scriptsrc="https://maps.googleapis.com/maps/api/js?key=AIzaSyAKFWBqlKAGCeS1rMVoaNlwyayu0e0YRes"></script>
<scriptsrc="js/map-custom.js"></script>
<!--===============================================================================================-->
<scriptsrc="js/main.js"></script>

<!--Globalsitetag(gtag.js)-GoogleAnalytics-->
<scriptasyncsrc="https://www.googletagmanager.com/gtag/js?id=UA-23581568-13"></script>
<script>
window.dataLayer=window.dataLayer||[];
functiongtag(){
dataLayer.push(arguments);
}
gtag('js',newDate());

gtag('config','UA-23581568-13');
</script>


</body>
</html>
```

#### addDoctor.jsp
- addDoctor.jsp
  - Description: Code from programlisting
  - Source Code:
```java
<%--
Document:UserHome
Createdon:13Aug,2020,9:56:36AM
Author:Admin
--%>

<%pagecontentType="text/html"pageEncoding="UTF-8"%>
<!DOCTYPEhtml>
<html>
<head>
<metahttp-equiv="Content-Type"content="text/html;charset=UTF-8">
<title>UserHome</title>
<linkrel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<linkrel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<link
href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
rel="stylesheet"id="bootstrap-css">
<script
src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<linkrel="stylesheet"type="text/css"href="css/adddataform.css">
<linkrel="stylesheet"type="text/css"href="css/adddatafrm1.css">
<style>
body{
background-image:url("img/Medical.jpg");
background-color:#cccccc;
}
</style>
</head>
<body>
<navclass="navbarnavbar-expand-lgnavbar-lightbg-light">
<ahref="#"class="navbar-brand"><imgsrc="img/2855.jpeg"
height="30"width="100"alt="HospitalManagementSystem">
</a>
<buttonclass="navbar-toggler"type="button"data-toggle="collapse"data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent"aria-expanded="false"aria-label="Togglenavigation">
<spanclass="navbar-toggler-icon"></span>
</button>

<divclass="collapsenavbar-collapse"id="navbarSupportedContent">
<h3>
<b>HospitalManagementSystem</b>
</h3>
<ulclass="navbar-navml-auto"style="margin-right:70px;">

<liclass="nav-itemactive">
<aclass="nav-link"href="AdminHome.jsp">Home<spanclass="sr-only">(current)</span></a>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
PATIENT
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addpatient.jsp">AddPatient</a>
<aclass="dropdown-item"href="adminPatientList.jsp">PatientList</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
DOCTOR
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addDoctor.jsp">AddDoctor</a>
<aclass="dropdown-item"href="adminDoctorList.jsp">ViewDoctor</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
RECEPTIONIST
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addRecp.jsp">AddReceptionist</a>
<aclass="dropdown-item"href="adminRecpList.jsp">ViewReceptionist</a>
</div>
</li>
<liclass="nav-itemdropdown">
<aclass="nav-linkdropdown-toggle"href="#"id="navbarDropdown"role="button"data-toggle="dropdown"aria-haspopup="true"aria-expanded="false">
WORKER
</a>
<divclass="dropdown-menu"aria-labelledby="navbarDropdown">
<aclass="dropdown-item"href="addWorker.jsp">AddWorker</a>
<aclass="dropdown-item"href="adminWorkerList.jsp">ViewWorker</a>
</div>
</li>
</ul>
</div>
</nav>


<divclass="container-contact100">


<divclass="wrap-contact100">
<divclass="contact100-form-title"style="background-image:url(img/bg-01.jpg);">
<spanclass="contact100-form-title-1">
DoctorRegistrationForm
</span>
</div>

<formclass="contact100-formvalidate-form"action="<%=request.getContextPath()%>/AddDoctor"method="post">
<divclass="wrap-input100validate-input"data-validate="UniqeIDisrequired">
<spanclass="label-input100">Id</span>
<inputclass="input100"type="text"name="id"placeholder="EnterUniqeID">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="FirstNameisrequired">
<spanclass="label-input100">First_Name:</span>
<inputclass="input100"type="text"name="fname"placeholder="EnterFirstname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="LastNameisrequired">
<spanclass="label-input100">Last_Name:</span>
<inputclass="input100"type="text"name="lname"placeholder="EnterLastname">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="genderisrequired">
<spanclass="label-input100">Gender:</span>
<inputclass="input100"type="text"name="gender"placeholder="EnterGender">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Phoneisrequired">
<spanclass="label-input100">Phone:</span>
<inputclass="input100"type="text"name="Mobile"placeholder="Enterphonenumber">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Cityisrequired">
<spanclass="label-input100">City:</span>
<inputclass="input100"type="text"name="City"placeholder="EnterCity">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Validemailisrequired:exabc.xyz">
<spanclass="label-input100">Email:</span>
<inputclass="input100"type="text"name="email"placeholder="Enteremail">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Ageisrequired">
<spanclass="label-input100">Age:</span>
<inputclass="input100"type="text"name="age"placeholder="EnterAge">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="Addressisrequired">
<spanclass="label-input100">Address</span>
<inputclass="input100"type="text"name="address"placeholder="EnterAddress">
<spanclass="focus-input100"></span>
</div>

<divclass="wrap-input100validate-input"data-validate="qualificationisrequired">
<spanclass="label-input100">Qualification</span>
<inputclass="input100"type="text"name="qualification"placeholder="EnterQualification">
<spanclass="focus-input100"></span>
</div>

<divclass="container-contact100-form-btn">
<buttonclass="contact100-form-btn">
<span>
Submit
<iclass="fafa-long-arrow-rightm-l-7"aria-hidden="true"></i>
</span>
</button>
</div>
</form>
</div>
</div>



<divid="dropDownSelect1"></div>
<scriptsrc="https://maps.googleapis.com/maps/api/js?key=AIzaSyAKFWBqlKAGCeS1rMVoaNlwyayu0e0YRes"></script>
<scriptsrc="js/map-custom.js"></script>
<!--===============================================================================================-->
<scriptsrc="js/main.js"></script>

<!--Globalsitetag(gtag.js)-GoogleAnalytics-->
<scriptasyncsrc="https://www.googletagmanager.com/gtag/js?id=UA-23581568-13"></script>
<script>
window.dataLayer=window.dataLayer||[];
functiongtag(){
dataLayer.push(arguments);
}
gtag('js',newDate());

gtag('config','UA-23581568-13');
</script>


</body>
</html>
```

### Cluster 5
**Requirement:** This is a test requirement that includes the word calculate.

**Classes and Methods:**

#### context.xml
- context.xml
  - Description: Code from programlisting
  - Source Code:
```java
<?xmlversion="1.0"encoding="UTF-8"?>
<Contextpath="/HospitalManagementSystem"/>
```