//-----------------------------------------------------------------------------
//
//	Main.cpp
//
//	Minimal application to test OpenZWave.
//
//	Creates an OpenZWave::Driver and the waits.  In Debug builds
//	you should see verbose logging to the console, which will
//	indicate that communications with the Z-Wave network are working.
//
//	Copyright (c) 2010 Mal Lansell <mal@openzwave.com>
//
//
//	SOFTWARE NOTICE AND LICENSE
//
//	This file is part of OpenZWave.
//
//	OpenZWave is free software: you can redistribute it and/or modify
//	it under the terms of the GNU Lesser General Public License as published
//	by the Free Software Foundation, either version 3 of the License,
//	or (at your option) any later version.
//
//	OpenZWave is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU Lesser General Public License for more details.
//
//	You should have received a copy of the GNU Lesser General Public License
//	along with OpenZWave.  If not, see <http://www.gnu.org/licenses/>.
//
//-----------------------------------------------------------------------------

#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include "Options.h"
#include "Manager.h"
#include "Driver.h"
#include "Node.h"
#include "Group.h"
#include "Notification.h"
#include "ValueStore.h"
#include "Value.h"
#include "ValueBool.h"
#include "Log.h"


// Defines
// For Aeon Labs Door/Window Sensor, the following command classes send events
#define COMMAND_CLASS_BASIC 0x20
#define COMMAND_CLASS_SENSOR_BINARY 0x30
#define COMMAND_CLASS_WAKE_UP 0x84
#define COMMAND_CLASS_BATTERY 0x80
#define COMMAND_CLASS_ALARM 0x71
#define COMMAND_CLASS_VERSION 0x86

// For HSM-100, we have COMMAND_CLASS_BASIC, COMMAND_CLASS_BATTERY, COMMAND_CLASS_WAKE_UP,
// COMMAND_CLASS_VERSION, and the following classes:
#define COMMAND_CLASS_CONFIGURATION 0x70
#define COMMAND_CLASS_SENSOR_MULTILEVEL 0x31
#define COMMAND_CLASS_MULTI_INSTANCE 0x60

using namespace OpenZWave;

static uint32 g_homeId = 0;
static bool   g_initFailed = false;

typedef struct
{
	uint32			m_homeId;
	uint8			m_nodeId;
	bool			m_polled;
	list<ValueID>	m_values;
}NodeInfo;

static list<NodeInfo*> g_nodes;
static pthread_mutex_t g_criticalSection;
static pthread_cond_t  initCond  = PTHREAD_COND_INITIALIZER;
static pthread_mutex_t initMutex = PTHREAD_MUTEX_INITIALIZER;

//-----------------------------------------------------------------------------
// <GetNodeInfo>
// Return the NodeInfo object associated with this notification
//-----------------------------------------------------------------------------
NodeInfo* GetNodeInfo
(
	Notification const* _notification
)
{
	uint32 const homeId = _notification->GetHomeId();
	uint8 const nodeId = _notification->GetNodeId();
	for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
	{
		NodeInfo* nodeInfo = *it;
		if( ( nodeInfo->m_homeId == homeId ) && ( nodeInfo->m_nodeId == nodeId ) )
		{
			return nodeInfo;
		}
	}

	return NULL;
}

//-----------------------------------------------------------------------------
// <OnNotification>
// Callback that is triggered when a value, group or node changes
//-----------------------------------------------------------------------------
void OnNotification
(
	Notification const* _notification,
	void* _context
)
{
	// Must do this inside a critical section to avoid conflicts with the main thread
	pthread_mutex_lock( &g_criticalSection );

    printf("_notification->GetType(): %d\n", _notification->GetType());

	switch( _notification->GetType() )
	{
		case Notification::Type_ValueAdded:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				// Add the new value to our list
				nodeInfo->m_values.push_back( _notification->GetValueID() );
			}
			break;
		}

		case Notification::Type_ValueRemoved:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				// Remove the value from out list
				for( list<ValueID>::iterator it = nodeInfo->m_values.begin(); it != nodeInfo->m_values.end(); ++it )
				{
					if( (*it) == _notification->GetValueID() )
					{
						nodeInfo->m_values.erase( it );
						break;
					}
				}
			}
			break;
		}

		case Notification::Type_ValueChanged:
		{
			// One of the node values has changed
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
                // Jason Tsao Changes
                
                printf("Jason: Got a ValueChanged!\n");

                printf("nodeID: %u\n", nodeInfo->m_nodeId);

                // Initialize values
                list<ValueID> valueIDList = nodeInfo->m_values;
                bool success = false;
                uint8 byte_value = 0;
                float float_value = 0.0;

                // Perform different actions based on which node
                switch(nodeInfo->m_nodeId) {
                    case 8: 
                        // Read the values in the node information
                        for( list<ValueID>::iterator it = valueIDList.begin(); it != valueIDList.end(); ++it) {

                            // Perform action based on CommandClassID
                            // For HSM-100, the following Classes need to be taken care of:
                            // 1. COMMAND_CLASS_BASIC (0x20)
                            // 2. COMMAND_CLASS_WAKE_UP (0x84)
                            // 3. COMMAND_CLASS_BATTERY (0x80)
                            // 4. COMMAND_CLASS_CONFIGURATION (0x70)
                            // 5. COMMAND_CLASS_SENSOR_MULTILEVEL (0x31)
                            // 6. COMMAND_CLASS_VERSION (0x86)
                            // 7. COMMAND_CLASS_CONFIGURATION (0x70)
                            // 8. COMMAND_CLASS_SENSOR_MULTILEVEL (0x31)

                            printf("CommandClassID: %x\n", it->GetCommandClassId());

                            switch(it->GetCommandClassId()) {
                                case COMMAND_CLASS_BASIC:
                                    printf("Jason: Got COMMAND_CLASS_BASIC!\n");
                                    printf("    Jason: ValueType: %d\n", (int) it->GetType());
                                    printf("    Jason: ValueGenre: %d\n", (int) it->GetGenre());
                                    printf("    Jason: Instance: %u\n", (uint8) it->GetInstance());
                                    printf("    Jason: ID: %u\n", (uint64) it->GetId());


                                    //printf("Event: %u", _notification->GetEvent());
                                    //if(_notification->GetEvent()) {
                                    //    printf("Door is Open!\n");
                                    //}
                                    //else {
                                    //    printf("Door is Closed!\n");
                                    //}

                                    break;
                                case COMMAND_CLASS_SENSOR_MULTILEVEL:
                                    printf("Jason: Got COMMAND_CLASS_SENSOR_MULTILEVEL!\n");
                                    printf("    Jason: ValueType: %d\n", (int) it->GetType());
                                    printf("    Jason: ValueGenre: %d\n", (int) it->GetGenre());
                                    printf("    Jason: Instance: %u\n", (uint8) it->GetInstance());
                                    printf("    Jason: ID: %u\n", (uint64) it->GetId());

                                    switch((int) it->GetType()) {
                                        // See open-zwave/cpp/src/value_classes/ValueID.h for ValueType enum 
                                        case 1:
                                            // Byte Type
                                            success = Manager::Get()->GetValueAsByte(*it, &byte_value);
                                            printf("Successfully got Value? %s\n", (success)?"Yes":"No");

                                            printf("Byte Read: %u\n", byte_value);

                                            break;
                                        case 2:
                                            // Decimal Type
                                            success = Manager::Get()->GetValueAsFloat(*it, &float_value);
                                            printf("Successfully got Value? %s\n", (success)?"Yes":"No");

                                            printf("Decimal Read: %f\n", float_value);
                                            break;
                                        default:
                                            printf("Unrecognized Type\n");
                                            break;
                                    }




                                    break;
                                case COMMAND_CLASS_CONFIGURATION:
                                    printf("Jason: Got COMMAND_CLASS_CONFIGURATION!\n");
                                    break;
                                case COMMAND_CLASS_WAKE_UP:
                                    printf("Jason: Got COMMAND_CLASS_WAKE_UP!\n");
                                    break;
                                case COMMAND_CLASS_BATTERY:
                                    printf("Jason: Got COMMAND_CLASS_BATTERY!\n");
                                    break;
                                case COMMAND_CLASS_VERSION:
                                    printf("Jason: Got COMMAND_CLASS_VERSION!\n");
                                    break;
                                default:
                                    printf("Jason: Got an Unknown COMMAND CLASS!\n");
                                    break;
                            }

                            printf("\n");
                            
                        }
                    break;
                    default:
                        printf("Unknown Node\n");
                        break;
                }


                printf("Jason: Finished ValueChanged\n");
                // Jason Tsao Changes End
			}
			break;
		}

		case Notification::Type_Group:
		{
			// One of the node's association groups has changed
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				nodeInfo = nodeInfo;		// placeholder for real action
			}
			break;
		}

		case Notification::Type_NodeAdded:
		{
			// Add the new node to our list
			NodeInfo* nodeInfo = new NodeInfo();
			nodeInfo->m_homeId = _notification->GetHomeId();
			nodeInfo->m_nodeId = _notification->GetNodeId();
			nodeInfo->m_polled = false;		
			g_nodes.push_back( nodeInfo );

            Manager::Get()->AddAssociation(nodeInfo->m_homeId, nodeInfo->m_nodeId, 1, 1);
			break;
		}

		case Notification::Type_NodeRemoved:
		{
			// Remove the node from our list
			uint32 const homeId = _notification->GetHomeId();
			uint8 const nodeId = _notification->GetNodeId();
			for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
			{
				NodeInfo* nodeInfo = *it;
				if( ( nodeInfo->m_homeId == homeId ) && ( nodeInfo->m_nodeId == nodeId ) )
				{
					g_nodes.erase( it );
					delete nodeInfo;
					break;
				}
			}
			break;
		}

		case Notification::Type_NodeEvent:
		{
			// We have received an event from the node, caused by a
			// basic_set or hail message.
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
                // Jason Tsao Changes
                
                printf("Jason: Got a NodeEvent!\n");

                printf("nodeID: %u\n", nodeInfo->m_nodeId);

                // Perform different actions based on which node
                switch(nodeInfo->m_nodeId) {
                    case 8: 
                    case 6:
                        // Read the values in the node information
                        list<ValueID> valueIDList = nodeInfo->m_values;
                        for( list<ValueID>::iterator it = valueIDList.begin(); it != valueIDList.end(); ++it) {

                            // Perform action based on CommandClassID
                            // For Aeon Labs Door/Window Sensor, there are 3 Class to take care of:
                            // 1. COMMAND_CLASS_BASIC (0x20)
                            // 2. COMMAND_CLASS_SENSOR_BINARY (0x30)
                            // 3. COMMAND_CLASS_WAKE_UP (0x84)
                            printf("CommandClassID: %x\n", it->GetCommandClassId());

                            switch(it->GetCommandClassId()) {
                                case COMMAND_CLASS_BASIC:
                                    printf("Jason: Got COMMAND_CLASS_BASIC!\n");
                                    printf("    Jason: ValueType: %d\n", (int) it->GetType());
                                    printf("    Jason: ValueGenre: %d\n", (int) it->GetGenre());
                                    printf("    Jason: Instance: %u\n", (uint8) it->GetInstance());
                                    printf("    Jason: ID: %u\n", (uint64) it->GetId());

                                    // COMMAND_CLASS_BASIC gives a boolean specifying if:
                                    // 0: Door is closed
                                    // 255: Door is open

                                    if(_notification->GetEvent()) {
                                        printf("Door is Open!\n");
                                    }
                                    else {
                                        printf("Door is Closed!\n");
                                    }

                                    break;
                                case COMMAND_CLASS_SENSOR_BINARY:
                                    printf("Jason: Got COMMAND_CLASS_SENSOR_BINARY!\n");
                                    break;
                                case COMMAND_CLASS_WAKE_UP:
                                    printf("Jason: Got COMMAND_CLASS_WAKE_UP!\n");
                                    break;
                                case COMMAND_CLASS_BATTERY:
                                    printf("Jason: Got COMMAND_CLASS_BATTERY!\n");
                                    break;
                                case COMMAND_CLASS_ALARM:
                                    printf("Jason: Got COMMAND_CLASS_ALARM!\n");
                                    break;
                                case COMMAND_CLASS_VERSION:
                                    printf("Jason: Got COMMAND_CLASS_VERSION!\n");
                                    break;
                                default:
                                    printf("Jason: Got an Unknown COMMAND CLASS!\n");
                                    break;
                            }


                            printf("\n");
                            
                        }
                    break;
                }


                printf("Jason: Finished NodeEvent\n");
                // Jason Tsao Changes End
			}
			break;
		}

		case Notification::Type_PollingDisabled:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				nodeInfo->m_polled = false;
			}
			break;
		}

		case Notification::Type_PollingEnabled:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				nodeInfo->m_polled = true;
			}
			break;
		}

		case Notification::Type_DriverReady:
		{
			g_homeId = _notification->GetHomeId();
			break;
		}

		case Notification::Type_DriverFailed:
		{
			g_initFailed = true;
			pthread_cond_broadcast(&initCond);
			break;
		}

		case Notification::Type_AwakeNodesQueried:
		case Notification::Type_AllNodesQueried:
		{
			pthread_cond_broadcast(&initCond);
			break;
		}

		case Notification::Type_DriverReset:
		case Notification::Type_MsgComplete:
		case Notification::Type_NodeNaming:
		case Notification::Type_NodeProtocolInfo:
		case Notification::Type_NodeQueriesComplete:
		default:
		{
		}
	}

	pthread_mutex_unlock( &g_criticalSection );
}

//-----------------------------------------------------------------------------
// <main>
// Create the driver and then wait
//-----------------------------------------------------------------------------
int main( int argc, char* argv[] )
{
	pthread_mutexattr_t mutexattr;

	pthread_mutexattr_init ( &mutexattr );
	pthread_mutexattr_settype( &mutexattr, PTHREAD_MUTEX_RECURSIVE );
	pthread_mutex_init( &g_criticalSection, &mutexattr );
	pthread_mutexattr_destroy( &mutexattr );

	pthread_mutex_lock( &initMutex );

	// Create the OpenZWave Manager.
	// The first argument is the path to the config files (where the manufacturer_specific.xml file is located
	// The second argument is the path for saved Z-Wave network state and the log file.  If you leave it NULL 
	// the log file will appear in the program's working directory.
	Options::Create( "../../../../config/", "", "" );
	Options::Get()->AddOptionInt( "SaveLogLevel", LogLevel_Detail );
	Options::Get()->AddOptionInt( "QueueLogLevel", LogLevel_Debug );
	Options::Get()->AddOptionInt( "DumpTrigger", LogLevel_Error );
	Options::Get()->AddOptionInt( "PollInterval", 500 );
	Options::Get()->AddOptionBool( "IntervalBetweenPolls", true );
	Options::Get()->AddOptionBool("ValidateValueChanges", true);
	Options::Get()->Lock();

	Manager::Create();

	// Add a callback handler to the manager.  The second argument is a context that
	// is passed to the OnNotification method.  If the OnNotification is a method of
	// a class, the context would usually be a pointer to that class object, to
	// avoid the need for the notification handler to be a static.
	Manager::Get()->AddWatcher( OnNotification, NULL );

	// Add a Z-Wave Driver
	// Modify this line to set the correct serial port for your PC interface.

	string port = "/dev/ttyUSB0";
	if ( argc > 1 )
	{
		port = argv[1];
	}
	if( strcasecmp( port.c_str(), "usb" ) == 0 )
	{
		Manager::Get()->AddDriver( "HID Controller", Driver::ControllerInterface_Hid );
	}
	else
	{
		Manager::Get()->AddDriver( port );
	}

	// Now we just wait for either the AwakeNodesQueried or AllNodesQueried notification,
	// then write out the config file.
	// In a normal app, we would be handling notifications and building a UI for the user.
	pthread_cond_wait( &initCond, &initMutex );

	// Since the configuration file contains command class information that is only 
	// known after the nodes on the network are queried, wait until all of the nodes 
	// on the network have been queried (at least the "listening" ones) before
	// writing the configuration file.  (Maybe write again after sleeping nodes have
	// been queried as well.)
	if( !g_initFailed )
	{

		Manager::Get()->WriteConfig( g_homeId );

		// The section below demonstrates setting up polling for a variable.  In this simple
		// example, it has been hardwired to poll COMMAND_CLASS_BASIC on the each node that 
		// supports this setting.
		pthread_mutex_lock( &g_criticalSection );
		for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
		{
			NodeInfo* nodeInfo = *it;

			// skip the controller (most likely node 1)
			if( nodeInfo->m_nodeId == 1) continue;

			for( list<ValueID>::iterator it2 = nodeInfo->m_values.begin(); it2 != nodeInfo->m_values.end(); ++it2 )
			{
				ValueID v = *it2;
				if( v.GetCommandClassId() == 0x20 )
				{
					Manager::Get()->EnablePoll( v, 2 );		// enables polling with "intensity" of 2, though this is irrelevant with only one value polled
					break;
				}
			}
		}
		pthread_mutex_unlock( &g_criticalSection );

		// If we want to access our NodeInfo list, that has been built from all the
		// notification callbacks we received from the library, we have to do so
		// from inside a Critical Section.  This is because the callbacks occur on other 
		// threads, and we cannot risk the list being changed while we are using it.  
		// We must hold the critical section for as short a time as possible, to avoid
		// stalling the OpenZWave drivers.
		// At this point, the program just waits for 3 minutes (to demonstrate polling),
		// then exits
		for( int i = 0; i < 60*3; i++ )
		{
			pthread_mutex_lock( &g_criticalSection );
			// but NodeInfo list and similar data should be inside critical section
			pthread_mutex_unlock( &g_criticalSection );
			sleep(1);
		}

		Driver::DriverData data;
		Manager::Get()->GetDriverStatistics( g_homeId, &data );
		printf("SOF: %d ACK Waiting: %d Read Aborts: %d Bad Checksums: %d\n", data.s_SOFCnt, data.s_ACKWaiting, data.s_readAborts, data.s_badChecksum);
		printf("Reads: %d Writes: %d CAN: %d NAK: %d ACK: %d Out of Frame: %d\n", data.s_readCnt, data.s_writeCnt, data.s_CANCnt, data.s_NAKCnt, data.s_ACKCnt, data.s_OOFCnt);
		printf("Dropped: %d Retries: %d\n", data.s_dropped, data.s_retries);
	}

	// program exit (clean up)
	if( strcasecmp( port.c_str(), "usb" ) == 0 )
	{
		Manager::Get()->RemoveDriver( "HID Controller" );
	}
	else
	{
		Manager::Get()->RemoveDriver( port );
	}
	Manager::Get()->RemoveWatcher( OnNotification, NULL );
	Manager::Destroy();
	Options::Destroy();
	pthread_mutex_destroy( &g_criticalSection );
	return 0;
}
