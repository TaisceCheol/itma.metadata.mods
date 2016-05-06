<xsl:stylesheet version="2.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:mods="http://www.loc.gov/mods/v3"
	exclude-result-prefixes="mods">
	<xsl:output method="xml" indent="yes"/>

	<xsl:template match="mods:modsCollection">
		<add>
			<xsl:apply-templates select="mods:mods"/>
		</add>
	</xsl:template>

	<xsl:template match="mods:mods">
		<doc>
			<xsl:apply-templates select="mods:identifier[@type = 'local']"/>
			<xsl:apply-templates select="mods:titleInfo"/>
			<xsl:apply-templates select="mods:note[@type = 'statement of responsibility']"/>
			<xsl:apply-templates select="mods:language"/>
			<xsl:apply-templates select="mods:subject/mods:topic"/>
			<xsl:apply-templates select="mods:subject/mods:geographic"/>
			<!-- <xsl:apply-templates select="mods:originInfo[@eventType = 'publication']"/> -->
			<xsl:apply-templates select="mods:typeOfResource"/>
			<xsl:apply-templates select="mods:abstract"/>
			<xsl:apply-templates select="mods:physicalDescription/mods:extent"/>
			<xsl:apply-templates select="mods:physicalDescription/mods:note[@type = 'running-time']"/>
			<xsl:apply-templates select="mods:accessCondition"/>
			<xsl:apply-templates select="mods:genre"/>
			<xsl:apply-templates select="mods:tableOfContents"/>
		</doc>
	</xsl:template>

	<xsl:template match="mods:identifier[@type = 'local']">
		<xsl:if test="starts-with(., 'CID-')">
			<field name="id">itma:cid:<xsl:value-of select="substring-after(., 'CID-')"/></field>
		</xsl:if>
	</xsl:template>

	<xsl:template match="mods:titleInfo">
		<field name="title_display">
			<xsl:value-of select="./mods:title"/>
		</field>
	</xsl:template>

	<xsl:template match="mods:titleInfo[@type = 'alternative']">
		<field name="subtitle_display">
			<xsl:value-of select="./mods:title"/>
		</field>
	</xsl:template>

	<xsl:template match="mods:note[@type = 'statement of responsibility']">
		<field name="author_display">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:language">
		<xsl:for-each select="./mods:languageTerm">
			<field name="language_facet">
				<xsl:value-of select="."/>
			</field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:subject/mods:topic">
		<xsl:for-each select=".">
			<field name="subject_topic_facet">
				<xsl:value-of select="."/>
			</field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:subject/mods:geographic">
		<xsl:for-each select=".">
			<field name="subject_geo_facet">
				<xsl:value-of select="."/>
			</field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:originInfo[@eventType = 'publication']">
		<xsl:for-each select="./mods:dateIssued">
			<field name="pub_date">
				<xsl:value-of select="."/>
			</field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:typeOfResource">
		<field name="format">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:abstract">
		<field name="abstract_t">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:physicalDescription/mods:extent">
		<field name="physical_description_s">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:physicalDescription/mods:note[@type = 'running-time']">
		<field name="running_time_s">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:accessCondition">
		<xsl:for-each select=".">
			<field name="copyright_s">
				<xsl:value-of select="."/>
			</field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:genre">
		<field name="material_facet">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:tableOfContents">
		<field name="contents_txt">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

</xsl:stylesheet>
