name := "SimpleCrudApp"

version := "0.1"

scalaVersion := "2.12.8"

val domain = "jhole89"
lazy val root = (project in file(".")).enablePlugins(PlayScala)

addCommandAlias("sanity", ";clean ;compile ;assembly ;test ;coverage ;coverageReport ;scalastyle")

resolvers in Global ++= Seq(
  "sonatype-releases" at "https://oss.sonatype.org/content/repositories/releases/"
)

libraryDependencies ++= applicationDependencies ++ testDependencies

val applicationDependencies = Seq(
  guice,
  "com.typesafe.play" %% "play-slick" % "4.0.0",
  "com.typesafe.play" %% "play-slick-evolutions" % "4.0.0",
)

val testDependencies = Seq(
  "org.pegdown" % "pegdown" % "1.6.0" % "test",
  "org.scalatest" % "scalatest_2.12" % "3.0.5" % "test",
)

testOptions in Test ++= Seq(
  Tests.Argument(TestFrameworks.ScalaTest, "-o"),
  Tests.Argument(TestFrameworks.ScalaTest, "-h", "target/test-reports")
)

parallelExecution in Test := false
fork in Test := true
javaOptions += "-Xmx2G"
