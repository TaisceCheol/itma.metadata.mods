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
			<!-- <xsl:apply-templates select="mods:name"/> -->
			<!-- <xsl:apply-templates select="mods:note[@type = 'statement of responsibility']"/> -->
<!-- 			<xsl:apply-templates select="mods:language"/>
			<xsl:apply-templates select="mods:subject/mods:topic"/>
			<xsl:apply-templates select="mods:subject/mods:geographic"/>
			<xsl:apply-templates select="mods:originInfo[@eventType = 'publication']"/>
			<xsl:apply-templates select="mods:typeOfResource"/>
			<xsl:apply-templates select="mods:abstract"/>
			<xsl:apply-templates select="mods:physicalDescription/mods:extent"/>
			<xsl:apply-templates select="mods:physicalDescription/mods:note[@type = 'running-time']"/>
			<xsl:apply-templates select="mods:accessCondition"/>
			<xsl:apply-templates select="mods:genre"/> -->
<!--			<xsl:apply-templates select="mods:tableOfContents"/>-->
			<!-- <xsl:apply-templates select="mods:relatedItem[@displayLabel='Collection']/mods:titleInfo/mods:title"/> -->
			<xsl:apply-templates select="mods:relatedItem[@type='constituent']/mods:titleInfo/mods:title"/>
			<!-- <xsl:apply-templates select="mods:location/mods:holdingSimple/mods:shelfLocator"/> -->
			<!-- <xsl:apply-templates select="mods:location/mods:url"/> -->
		</doc>
	</xsl:template>

	<xsl:template match="mods:identifier[@type = 'local']">
		<xsl:if test="starts-with(., 'CID-')">
			<field name="id">itma:cid:<xsl:value-of select="substring-after(., 'CID-')"/></field>
		</xsl:if>
		<xsl:if test="not(starts-with(., 'CID-'))">
			<field name="itma_reference_display"><xsl:value-of select="."/></field>
		</xsl:if>		
	</xsl:template>

	<xsl:template match="mods:titleInfo[@type='alternative']">
		<field name="alt_title_display"><xsl:value-of select="./mods:title"/></field>
		<field name="alt_title_t"><xsl:value-of select="./mods:title"/></field>
	</xsl:template>

	<xsl:template match="mods:titleInfo">
		<field name="title_display"><xsl:value-of select="./mods:title"/></field>
		<field name="title_t"><xsl:value-of select="./mods:title"/></field>
	</xsl:template>

<!-- 	<xsl:template match="mods:titleInfo[@type = 'alternative']">
		<field name="subtitle_display">
			<xsl:value-of select="./mods:title"/>
		</field>
	</xsl:template> -->

	<xsl:template match="mods:name">
		<xsl:if test="./mods:namePart[@type]">
			<field name="people_display">
				<xsl:value-of select="./mods:namePart[@type='given']"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="./mods:namePart[@type='family']"/>
			</field>			
			<field name="people_t">
				<xsl:value-of select="./mods:namePart[@type='given']"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="./mods:namePart[@type='family']"/>
			</field>
			<field name="people_facet">
				<xsl:value-of select="./mods:namePart[@type='given']"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="./mods:namePart[@type='family']"/>
			</field>			
		</xsl:if>
	</xsl:template>

	<xsl:template match="mods:note[@type = 'statement of responsibility']">
		<field name="author_display"><xsl:value-of select="."/></field>
		<field name="author_t"><xsl:value-of select="."/></field>
	</xsl:template>

	<xsl:template match="mods:name[mods:role]">
		<xsl:if test="./mods:role/mods:roleTerm/text() = 'Creator'">
			<field name="author_display"><xsl:value-of select="./mods:namePart"/></field>
			<field name="author_t"><xsl:value-of select="./mods:namePart"/></field>
		</xsl:if>
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
			<xsl:choose>
				<xsl:when test="substring-before(.,'-')">
					<field name="pub_date"><xsl:value-of select="substring-before(.,'-')"/></field>
					<field name="pub_date_sort"><xsl:value-of select="number(substring-before(.,'-'))"/></field>
				</xsl:when>
				<xsl:otherwise>
					<field name="pub_date"><xsl:value-of select="."/></field>
					<field name="pub_date_sort"><xsl:value-of select="."/></field>					
				</xsl:otherwise>
			</xsl:choose>
			<field name="pub_date_display"><xsl:value-of select="."/></field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:typeOfResource">
		<field name="format">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>

	<xsl:template match="mods:abstract">
		<field name="abstract_txt">
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
			<field name="copyright_t">
				<xsl:value-of select="."/>
			</field>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mods:genre">
		<field name="material_facet">
			<xsl:value-of select="."/>
		</field>
		<field name="material_display">
			<xsl:value-of select="."/>
		</field>		
	</xsl:template>

<!--	<xsl:template match="mods:tableOfContents">
		<field name="contents_txt">
			<xsl:value-of select="."/>
		</field>
	</xsl:template>-->

	<xsl:template match="mods:relatedItem[@displayLabel='Collection']/mods:titleInfo/mods:title">
		<field name="collection_facet">
			<xsl:value-of select="."/>
		</field>
		<field name="collection_t">
			<xsl:value-of select="."/>
		</field>	
		<field name="collection_display">
			<xsl:value-of select="."/>
		</field>	
	</xsl:template>
	
	<xsl:template match="mods:relatedItem[@type='constituent']/mods:titleInfo/mods:title">
		<field name="contents_t">
			<xsl:value-of select="."/>
		</field>	
		<field name="contents_facet">
			<xsl:value-of select="."/>
		</field>			
	</xsl:template>	
	
	<xsl:template match="mods:location/mods:holdingSimple/mods:shelfLocator">
		<!-- Use this facet to	facet items in archive and not in archive	-->
		<field name="archive_location_facet"></field>
		<field name="archive_location_display"><xsl:value-of select="."/></field>
	</xsl:template>

	<xsl:template match="mods:location/mods:url">
		<field name="object_url_display"><xsl:value-of select="."/></field>
		<field name="digitized_facet">Digitized</field>
	</xsl:template>

</xsl:stylesheet>
