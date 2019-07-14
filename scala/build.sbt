name := "SimpleCrudApp"

version := "0.1"

scalaVersion := "2.13.0"

val domain = "jhole89"
lazy val root = (project in file(".")).enablePlugins(PlayScala)

addCommandAlias("sanity", ";clean ;compile ;test ;coverage ;coverageReport ;scalastyle")

resolvers in Global ++= Seq(
  "sonatype-releases" at "https://oss.sonatype.org/content/repositories/releases/"
)

libraryDependencies ++= applicationDependencies ++ testDependencies

val applicationDependencies = Seq(
  guice,
  "com.typesafe.play" %% "play-slick" % "4.0.2",
  "com.typesafe.play" %% "play-slick-evolutions" % "4.0.2"
)

val testDependencies = Seq(
  "com.h2database" % "h2" % "1.4.199",
  specs2 % Test
)

testOptions in Test ++= Seq(
  Tests.Argument(TestFrameworks.ScalaTest, "-o"),
  Tests.Argument(TestFrameworks.ScalaTest, "-h", "target/test-reports")
)

scalacOptions ++= Seq(
  "-feature",
  "-deprecation",
  "-Xfatal-warnings"
)
